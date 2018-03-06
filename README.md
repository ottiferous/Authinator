# Authinator
End User verification for Help Desks using Duo

The application begins by getting a username within your Duo instance. This will repeat until a valid username is found, or you press 'q'. The available devices for that user will be displayed, and the user can then choose which device, followed by which vailable method you want to use for that device.

The status of any Authentication (e.g. user chooses approve or deny) will be displayed as the result. Please note "Login request denied." and "Reporting login as fraudulent." are both the result of the end user denying the request. This is shown in the example workflow at the bottom of this readme.

Ctrl + C can be used at any time to quit the application, otherwise it will repeatedly loop to allow authentication of mulitple users.

## Example workflow
Type the user's name in Duo: andrew

0. Andrew's TestPhone (XXX-XXX-1234)
1. Chewbacca (iOS)
2. token 4177714

Authenticate with device # 0

0. auto
1. push
2. sms
3. phone
4. mobile_otp

Authenticate with method # 3

Authenticating with phone

Reporting login as fraudulent.
