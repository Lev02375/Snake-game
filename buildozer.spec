name: Build APK

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Set up Android SDK
      uses: android-actions/setup-android@v3
      with:
        packages: 'platforms;android-30 build-tools;30.0.3'

    - name: Accept Android licenses
      run: yes | $ANDROID_HOME/tools/bin/sdkmanager --licenses || true

    - name: Install dependencies
      run: |
        sudo apt update
        sudo apt install -y zlib1g-dev libffi-dev libssl-dev
        pip install buildozer cython pygame

    - name: Build APK
      run: |
        export ANDROID_HOME=$ANDROID_HOME
        buildozer android debug --no-deploy

    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: snake-game
        path: bin/*.apk
