[app]

# (str) Title of your application
title = Boss Battle

# (str) Package name
package.name = bossbattle

# (str) Package domain (needed for android/ios packaging)
package.domain = org.yourname

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 0.2

#apk name
android.release_name = bossbattle-0.2.apk

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientation
orientation = portrait

# (list) List of allowed orientations
orientation.Landscape = False
orientation.Portrait = True

# (bool) Indicate if the application should be fullscreen or not
fullscreen = False

[android]

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android NDK version to use
android.ndk = 25b

# (str) Android build tools version
android.build_tools = 33.0.2

# (list) Permissions
android.permissions = 

# (list) Android archs
android.archs = arm64-v8a,armeabi-v7a

# (str) Android SDK path (leave empty for auto-detection)
# android.sdk_path = 

# (str) Android NDK path (leave empty for auto-detection)
# android.ndk_path =