# FastVision: Teacher Certification Validation Tool

## Overview

FastVision is a solution designed to automate the teacher verification process for PlayPickleball. It utilizes OpenAI's GPT-4 Vision Preview model 
to reliably classify and verify teacher certification images uploaded during the onboarding process. The tool analyzes the images, 
checks if they are valid certifications, and confirms if they match the accepted list of teacher certifications.

## Problem Statement

Previously, the teacher verification process at PlayPickleball involved a manual review of the teacher certification images uploaded by applicants. 
A member of the programs team or a developer would manually assess the images and update the `verified` column in the Supabase database accordingly.

## Solution

FastVision streamlines this process by leveraging the GPT-4 Vision Preview model's image classification and verification capabilities. 
The solution involves the following steps:

1. Connecting to the Supabase.py SDK to retrieve the uploaded images from a given teacher application.
2. Bundling the images into a payload along with a prompt (see [main.py](./app/main.py)).
3. Sending the payload to the GPT-4 Vision Preview model and receiving the JSON response in the following format:
    ```bash

    HTTP/1.1 200 OK
    Content-Length: 283
    Content-Type: application/json
    Date: Sat, 09 Mar 2024 17:34:04 GMT
    Server: uvicorn

    {
        "content": "Validity: False (The second image is not the same as the first.)\n
        Confidence Rating: High (The design, text, and names on the certifications are clearly different.)\n\n
        Certified Instructor: The certification in the first image is given to Renata Simpson."
    }

    ```

4. Analyzing the response to determine if the images are valid certifications and fall within the accepted list.
6. Implementing additional logic to handle confidence ratings, where low-confidence responses can be forwarded to a Power App for manual review. 
   and high confidence ratings can be automated to `verified`.

## Installation

FastVision is built using Nix and Poetry via [poetry2nix](https://github.com/nix-community/poetry2nix). However, you can also clone the 
repository and install the dependencies manually:

```bash
git clone --depth 1 git@github.com:selkirksport/SPIKE---teacher-validation-via-openai-vision.git
```

If you have [nix](https://nixos.org/) with flakes enabled, then all you have to do is:

```bash
nix develop
```

If you do not have nix then the manual route works just fine:

### Install Poetry 
Through one of the recommended [means](https://python-poetry.org/docs/), and then install the app dependencies using Poetry:

```bash
poetry install
```
Make sure to handle any potential Python version conflicts that may arise.

## Running the Application
To run the application, `chmod` and execute the provided dev script:

```bash
chmod +x dev
./dev

```

This will start the server.

### Testing the Endpoint
You can test the endpoint by sending a cURL or HTTPie request:

Using cURL:

```bash
curl -X 'POST' \
'http://127.0.0.1:8000/validate_images/' \
-H 'accept: application/json' \
-H 'Content-Type: multipart/form-data' \
-F 'model=gpt-4-vision-preview' \
-F 'prompt=Return three Ratings: Validity, as a bool, whether the second image is the same as the first, Confidence Rating, indicate a confidence rating concerning the Validity response, Certified Instructor, output to whom, on the first image the certification is given to.' \
-F 'images=@data/pci_true.jpeg;type=image/jpeg' \
-F 'images=@data/pci_false_ppr.jpeg;type=image/jpeg'

```
Using [HTTPie](https://httpie.io/):

```bash
http --form POST http://127.0.0.1:8000/validate_images/ \
accept:application/json \
Content-Type:multipart/form-data \
model='gpt-4-vision-preview' \
prompt='Return three Ratings: Validity, as a bool, whether the second image is the same as the first, Confidence Rating, indicate a confidence rating concerning the Validity response, Certified Instructor, output to whom, on the first image the certification is given to.' \
images@data/pci_true.jpeg \
images@data/pci_false_ppr.jpeg
```

## TODO
At the moment there is little to no error handling:
    - what happens if the data is corrupted on transmission?
    - validation for the correctness of configuration variables
    - validation errors for models 
    - too large file sizes
    - unsupported file formats for images could cause the encoder to fail
    - api rate limits, api key expiration
    - logging, client friendly error messages, and monitoring of app
    - race conditions: make the application stateless (asyncio.Lock)
    - external api calls: state dependency



## Further Reading
- [Poetry](https://python-poetry.org/docs/)
- [Nix](https://nixos.org/)
- [poetry2nix](https://github.com/nix-community/poetry2nix)
- [HTTPie](https://httpie.io/)
