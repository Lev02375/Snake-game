[app]

title = SnakeGame
package.name = snakegame
package.domain = org.openclaude

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0
orientation = landscape
fullscreen = 1

# Permissions
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Requirements
# Note: pygame is used for the game, which is compatible with Android
requirements = python3, pygame

# Android SDK
android.sdk = 33
android.ndk = 25b
android.minapi = 21
android.targetapi = 33

# Build settings
android.arch = arm64-v8a
p4a.branch = master
p4a.bootstrap = sdl2

# Icons
icon.filename = assets/icon.png

# Logs
log_level = 2

# Misc
show.pyinstallerdirs = 1
android.release_artifact =
