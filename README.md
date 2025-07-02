# AI Photo Enhancer
A web app to enhance multiple photos using GFPGAN via Replicate API.

## Setup
1. Clone the repository: `git clone https://github.com/your-username/photo-enhancer.git`
2. Create a `.env` file with `REPLICATE_API_TOKEN=your_token`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run locally: `python app.py`.

## Deployment
- Deploy on Render.com using the provided Dockerfile.
- Set `REPLICATE_API_TOKEN` in Render’s environment variables.

## Usage
- Visit the deployed URL.
- Upload up to 20 PNG/JPG images.
- Download enhanced images as a .zip file.
