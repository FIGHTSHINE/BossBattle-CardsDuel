[app]

# (str) Title of your application
title = Boss Battle beta-0.3

# (str) Package name
package.name = bossbattle

# (str) Package domain (needed for android/ios packaging)
package.domain = org.yourname

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 0.3

# apk name
android.file_name = bossbattle-0.3.apk

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientation (landscape for optimal gameplay experience)
# Options: portrait, landscape, or all (for auto-rotation)
orientation = landscape

# (list) List of allowed orientations
orientation.Landscape = True
orientation.Portrait = False

# (bool) Indicate if the application should be fullscreen or not
fullscreen = False

[android]

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android NDK version to use
# android.ndk = 25b
android.ndk = 26b

# (str) Android build tools version
android.build_tools = 33.0.2

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,WAKE_LOCK

# (list) Android archs
# android.archs = arm64-v8a,armeabi-v7a
android.archs = arm64-v8a

# (str) Android SDK path (leave empty for auto-detection)
# android.sdk_path = 

# (str) Android NDK path (leave empty for auto-detection)
# android.ndk_path =

# Include fonts in APK
include_exts = png,jpg,kv,atlas,ttf,otf

# background-color
android.presplash_color = #000000

# ci keep light
android.wakelock = True