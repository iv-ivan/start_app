# CI/CD
1) Now we're going to setup [Github Actions](https://github.com/features/actions) as CI/CD
2) `mkdir -p .github/workflows`
3) Check `.github/workflows/test.yml` file. It includes linters, formatting checks and test runs.
4) Now each time you create new PR, you will see GA checks:

Broken tests:

<img width="400" alt="Screenshot 2025-01-26 at 21 19 45" src="https://github.com/user-attachments/assets/fe2d2ffe-8a54-4fa2-861a-d77fe5324689" />\
<img width="400" alt="Screenshot 2025-01-26 at 21 19 53" src="https://github.com/user-attachments/assets/d24ab162-83ce-41ca-a3d1-f7512dfced8c" />

Successful tests:

<img width="400" alt="Screenshot 2025-01-26 at 21 21 05" src="https://github.com/user-attachments/assets/521b171d-2c70-44c1-9520-ad5c32487828" />



