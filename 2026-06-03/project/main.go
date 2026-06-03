// URL Shortener API — Go (Wed 2026-06-03)
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"os"
	"os/signal"
	"strings"
	"sync"
	"syscall"
	"time"
)

const (
	defPort = ":8080"
	b62     = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
	scLen   = 7
)

type Record struct {
	ID, URL  string
	Created  time.Time
	Clicks   int64
}
type CreateReq struct{ URL string }
type CreateRsp struct{ Short, ID string }
type ErrRsp struct{ Error string }
type StatsRsp struct{ Total int; Clicks int64; Uptime int64 }

type Store struct {
	mu    sync.RWMutex
	data  map[string]*Record
	start time.Time
}

func NewStore() *Store {
	return &Store{data: make(map[string]*Record), start: time.Now()}
}

func (s *Store) Put(r *Record) error {
	s.mu.Lock(); defer s.mu.Unlock()
	if _, ok := s.data[r.ID]; ok { return fmt.Errorf("exists") }
	s.data[r.ID] = r; return nil
}

func (s *Store) Get(id string) (*Record, bool) {
	s.mu.RLock(); defer s.mu.RUnlock()
	r, ok := s.data[id]; return r, ok
}

func (s *Store) Click(id string) {
	s.mu.Lock(); defer s.mu.Unlock()
	if r, ok := s.data[id]; ok { r.Clicks++ }
}

func (s *Store) All() []*Record {
	s.mu.RLock(); defer s.mu.RUnlock()
	r := make([]*Record, 0, len(s.data))
	for _, v := range s.data { r = append(r, v) }
	return r
}

func (s *Store) Stats() StatsRsp {
	s.mu.RLock(); defer s.mu.RUnlock()
	var c int64
	for _, v := range s.data { c += v.Clicks }
	return StatsRsp{len(s.data), c, int64(time.Since(s.start).Seconds())}
}

func genShort() string {
	var sb strings.Builder
	for i := 0; i < scLen; i++ { sb.WriteByte(b62[rand.Intn(len(b62))]) }
	return sb.String()
}

func validURL(u string) bool {
	return strings.HasPrefix(u, "http://") || strings.HasPrefix(u, "https://")
}

type API struct {
	store *Store
	base  string
}

func NewAPI(s *Store, b string) *API {
	return &API{s, strings.TrimRight(b, "/")}
}

func (a *API) Create(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" { writeJSON(w, 405, ErrRsp{"method not allowed"}); return }
	var req CreateReq
	if json.NewDecoder(r.Body).Decode(&req) != nil || !validURL(req.URL) {
		writeJSON(w, 400, ErrRsp{"valid http/https URL required"}); return
	}
	var rec *Record
	for i := 0; i < 5; i++ {
		rec = &Record{genShort(), req.URL, time.Now(), 0}
		if a.store.Put(rec) == nil { break }
	}
	if rec == nil { writeJSON(w, 500, ErrRsp{"failed"}); return }
	writeJSON(w, 201, CreateRsp{fmt.Sprintf("%s/%s", a.base, rec.ID), rec.ID})
}

func (a *API) Resolve(w http.ResponseWriter, r *http.Request) {
	id := strings.TrimPrefix(r.URL.Path, "/")
	if id == "" { writeJSON(w, 400, ErrRsp{"missing code"}); return }
	rec, ok := a.store.Get(id)
	if !ok { writeJSON(w, 404, ErrRsp{"not found"}); return }
	a.store.Click(id); http.Redirect(w, r, rec.URL, 302)
}

func (a *API) Health(w http.ResponseWriter, r *http.Request) { writeJSON(w, 200, map[string]string{"s": "ok"}) }
func (a *API) Stats(w http.ResponseWriter, r *http.Request) { writeJSON(w, 200, a.store.Stats()) }
func (a *API) List(w http.ResponseWriter, r *http.Request) { writeJSON(w, 200, a.store.All()) }

func writeJSON(w http.ResponseWriter, s int, d interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(s); json.NewEncoder(w).Encode(d)
}

func logMW(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		t := time.Now(); next.ServeHTTP(w, r)
		log.Printf("%s %s %v", r.Method, r.URL.Path, time.Since(t))
	})
}

func main() {
	p := defPort
	if e := os.Getenv("PORT"); e != "" { p = ":" + e }
	s := NewStore()
	a := NewAPI(s, fmt.Sprintf("http://0.0.0.0%s", p))
	mux := http.NewServeMux()
	mux.HandleFunc("/api/shorten", a.Create)
	mux.HandleFunc("/api/stats", a.Stats)
	mux.HandleFunc("/api/urls", a.List)
	mux.HandleFunc("/api/health", a.Health)
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path == "/" { http.NotFound(w, r); return }
		a.Resolve(w, r)
	})
	srv := &http.Server{Addr: p, Handler: logMW(mux)}
	ch := make(chan os.Signal, 1)
	signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM)
	go func() { log.Printf("Started on %s", p); srv.ListenAndServe() }()
	<-ch; log.Println("Shutting"); srv.Close()
}
