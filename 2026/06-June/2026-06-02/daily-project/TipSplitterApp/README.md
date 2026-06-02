# 🧾 Tip Splitter — Android App

**Daily Project — June 2, 2026 (Tuesday: Java/Android)**

---

## 📱 Overview

Tip Splitter is a fully structured Android application that makes splitting restaurant bills effortless. Enter the bill amount, choose a tip percentage (10%, 15%, 20%, or custom), specify the number of people, and instantly see:

- 💵 **Tip Amount** — Calculated based on your chosen percentage
- 🧮 **Total with Tip** — Bill + tip combined
- 👥 **Per-Person Share** — Equal split among all diners

### Features

| Feature | Details |
|---------|---------|
| **Preset Tip Buttons** | Quick-select 10%, 15%, or 20% |
| **Custom Tip Entry** | Enter any tip percentage manually |
| **Input Validation** | Handles empty fields and invalid values gracefully |
| **Material Design UI** | Clean, modern Android interface |
| **Full APK Structure** | Ready to build with Android Studio or CLI |

---

## 🏗️ Project Structure

```
TipSplitterApp/
├── build.gradle                    # Root Gradle config
├── settings.gradle                 # Project settings
├── gradle.properties               # Gradle JVM settings
└── app/
    ├── build.gradle                # App module dependencies
    └── src/main/
        ├── AndroidManifest.xml     # App manifest
        ├── java/com/prashaanth/tipsplitter/
        │   └── MainActivity.java   # Main activity & logic
        └── res/
            ├── drawable/
            │   └── edit_text_bg.xml # Custom EditText style
            ├── layout/
            │   └── activity_main.xml # UI layout
            └── values/
                ├── colors.xml      # Color palette
                ├── strings.xml     # String resources
                └── themes.xml      # App theme
```

---

## 🚀 Building the APK

### Prerequisites
- [Android Studio](https://developer.android.com/studio) or
- [Android SDK Command Line Tools](https://developer.android.com/studio#command-line-tools-only)

### Build from Android Studio
1. Open `TipSplitterApp/` in Android Studio
2. Wait for Gradle sync
3. Click **Build → Build Bundle(s) / APK(s) → Build APK(s)**
4. APK is generated at `app/build/outputs/apk/debug/app-debug.apk`

### Build from CLI
```bash
cd TipSplitterApp
./gradlew assembleDebug
# APK: app/build/outputs/apk/debug/app-debug.apk
```

---

## 📸 Expected Behavior

```
Input:  Bill = $85.50, Tip = 15%, People = 4
Output: Tip Amount: $12.83
        Total: $98.33
        Each Pays: $24.58
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Java 11 |
| **UI Framework** | Android XML + Material Design |
| **Build System** | Gradle 8.2 |
| **Min SDK** | API 21 (Android 5.0) |
| **Target SDK** | API 34 (Android 14) |

---

*Daily Project # — Built on June 2, 2026*
