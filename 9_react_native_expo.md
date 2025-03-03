# Mobile app with React Native
1) React Native official documentation recommends us to use framework. We proceed with [Expo](https://docs.expo.dev/get-started/create-a-project/)
2) Create app:

```shell
mkdir mobile
cd mobile
npx create-expo-app@latest
```
3) Follow Expo guide to setup Development build for iOS+Android
   - Android: use the latest Android version available 
   - iOS: If you get `Xcode must be fully installed before you can continue. Continue to the App Store?`, you might need to run this: `sudo xcode-select -s /Applications/Xcode.app/Contents/Developer`
   - iOS: You might also need to install iOS components in XCode

4) Build:
```shell
npx expo run:android
npx expo run:ios
```

5) Android Emulator can't resolve `localhost` properly. To work with API running on `localhost` try:
```
# For localhost on Android proxy 8000 port:
adb devices
adb -s emulator-5554 reverse tcp:8000 tcp:8000
```
6) Check `app/(tabs)/*.tsx` files. I've patched app to look like our website from previous steps - the main changes are in `(tabs)/index.tsx`
7) Result:

<img width="405" alt="Screenshot 2025-03-05 at 20 25 05" src="https://github.com/user-attachments/assets/6f6b2575-9851-4f9d-abdc-d70e6cb3ea64" />
