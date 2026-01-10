from fastapi import APIRouter
from pydantic import BaseModel
import time

router = APIRouter(prefix="/ai", tags=["AI"])

class AIRequest(BaseModel):
    prompt: str
    context: str = ""

@router.post("/generate")
def generate_code(request: AIRequest):
    # Simulation of AI generation
    # in a real app, this would call OpenAI/Gemini/Anthropic API
    
    prompt_lower = request.prompt.lower()
    
    generated_code = ""
    if "docker" in prompt_lower:
        generated_code = """
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
"""
    elif "terraform" in prompt_lower:
        generated_code = """
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "DragonOpsWebServer"
  }
}
"""
    elif "nginx" in prompt_lower:
        generated_code = """
server {
    listen 80;
    server_name example.com;
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
"""
    else:
        generated_code = "# I'm sorry, I can only generate Docker, Terraform, or Nginx config at the moment."

    return {
        "code": generated_code,
        "explanation": "Here is the generated infrastructure code based on your request."
    }
