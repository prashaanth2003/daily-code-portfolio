package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

func setup() (*API, *Store) {
	s := NewStore(); return NewAPI(s, "http://localhost:8080"), s
}

func TestGenShort(t *testing.T) {
	for i := 0; i < 50; i++ {
		c := genShort()
		if len(c) != scLen { t.Fatal("bad len") }
		for _, ch := range c {
			if !strings.ContainsRune(b62, ch) { t.Fatal("bad char") }
		}
	}
}

func TestValidURL(t *testing.T) {
	for _, tc := range []struct{ u string; v bool }{
		{"https://go.dev", true}, {"http://go.dev", true},
		{"ftp://bad", false}, {"nope", false}, {"", false},
	} { if g := validURL(tc.u); g != tc.v { t.Errorf("%s: got %v", tc.u, g) } }
}

func TestStore(t *testing.T) {
	s := NewStore()
	if err := s.Put(&Record{"a", "https://a.com", time.Now(), 0}); err != nil {
		t.Fatal(err)
	}
	if err := s.Put(&Record{"a", "", time.Now(), 0}); err == nil { t.Fatal("expected dup error") }
	if _, ok := s.Get("a"); !ok { t.Fatal("should find") }
	if _, ok := s.Get("x"); ok { t.Fatal("should not find") }
	s.Click("a"); s.Click("a")
	r, _ := s.Get("a")
	if r.Clicks != 2 { t.Fatal("expected 2 clicks") }
}

func TestCreate(t *testing.T) {
	a, _ := setup()
	w := httptest.NewRecorder()
	a.Create(w, httptest.NewRequest("POST", "/", strings.NewReader(`{"url":"https://go.dev"}`)))
	if w.Code != 201 { t.Fatalf("expected 201, got %d", w.Code) }
	var r CreateRsp; json.NewDecoder(w.Body).Decode(&r)
	if r.ID == "" { t.Fatal("expected ID") }
}

func TestCreateInvalid(t *testing.T) {
	a, _ := setup()
	w := httptest.NewRecorder()
	a.Create(w, httptest.NewRequest("POST", "/", strings.NewReader(`{"url":"bad"}`)))
	if w.Code != 400 { t.Fatalf("expected 400, got %d", w.Code) }
}

func TestResolve404(t *testing.T) {
	a, _ := setup()
	w := httptest.NewRecorder()
	a.Resolve(w, httptest.NewRequest("GET", "/nonexist", nil))
	if w.Code != 404 { t.Fatalf("expected 404, got %d", w.Code) }
}

func TestStats(t *testing.T) {
	s := NewStore()
	s.Put(&Record{"a", "https://a.com", time.Now(), 0})
	s.Put(&Record{"b", "https://b.com", time.Now(), 0})
	s.Click("a")
	st := s.Stats()
	if st.Total != 2 || st.Clicks != 1 { t.Fatalf("got %d/%d", st.Total, st.Clicks) }
}

func TestConcurrent(t *testing.T) {
	s := NewStore()
	n := 50
	ch := make(chan bool, n)
	for i := 0; i < n; i++ {
		go func() { s.Put(&Record{genShort(), "https://x.com", time.Now(), 0}); ch <- true }()
	}
	for i := 0; i < n; i++ { <-ch }
	if st := s.Stats(); st.Total != n { t.Fatalf("expected %d, got %d", n, st.Total) }
}

func TestHealth(t *testing.T) {
	a, _ := setup()
	w := httptest.NewRecorder()
	a.Health(w, httptest.NewRequest("GET", "/", nil))
	if w.Code != 200 { t.Fatal("expected 200") }
}
