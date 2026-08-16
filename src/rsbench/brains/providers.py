"""Concrete contestant brains. Each only sets model_id/open-weight and wires _complete().

The _complete() bodies are STUBS: they read the provider API key and raise NotImplementedError
with the exact wiring TODO, so the package stays import-safe until you add the SDK calls.
Roster mirrors plan/v2/README.md.
"""
from __future__ import annotations

import os

from rsbench.brains.llm_base import LLMBrain


def _encode_image(image):
    """Return (bytes, mime) for a Gemini inline_data part, or None if there is no image."""
    if image is None:
        return None
    if isinstance(image, (bytes, bytearray)):
        return bytes(image), "image/jpeg"
    if isinstance(image, str):  # a file path
        import pathlib
        p = pathlib.Path(image)
        return p.read_bytes(), ("image/png" if p.suffix.lower() == ".png" else "image/jpeg")
    # numpy array or PIL image -> PNG via Pillow
    import io
    from PIL import Image  # type: ignore
    import numpy as np  # type: ignore
    img = image if isinstance(image, Image.Image) else Image.fromarray(np.asarray(image).astype("uint8"))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue(), "image/png"


class _Provider(LLMBrain):
    env_key: str = "UNSET_API_KEY"

    def _complete(self, prompt: str, image=None) -> str:
        key = os.environ.get(self.env_key)
        if not key:
            raise RuntimeError(f"set {self.env_key} to run {self.name}")
        raise NotImplementedError(
            f"TODO: call {self.name} ({self.model_id}) with temp=0 and return text. "
            f"Add the provider SDK call here."
        )


# --- general frontier brains (closed) ---
class GPT(_Provider):
    name, model_id, env_key, is_open_weight = "gpt", "gpt-5", "OPENAI_API_KEY", False

class Claude(_Provider):
    name, model_id, env_key, is_open_weight = "claude", "claude-opus-4-8", "ANTHROPIC_API_KEY", False

class Gemini(_Provider):
    name, model_id, env_key, is_open_weight = "gemini", "gemini-2.5-pro", "GEMINI_API_KEY", False

class GeminiER2(_Provider):
    """Robot-specialized brain; the step-1 default anchor (multimodal: image + text).

    Uses the Google Gen AI SDK (pip install google-genai). Key: https://aistudio.google.com/apikey
    """
    name, model_id, env_key, is_open_weight = "gemini-er2", "gemini-robotics-er-2-preview", "GEMINI_API_KEY", False

    def _complete(self, prompt: str, image=None) -> str:
        key = os.environ.get(self.env_key)
        if not key:
            raise RuntimeError(
                f"set {self.env_key} to run {self.name} - get a key at https://aistudio.google.com/apikey"
            )
        try:
            from google import genai  # pip install google-genai
        except ImportError as exc:
            raise ImportError("pip install google-genai to run gemini-er2") from exc
        parts: list = []
        blob = _encode_image(image)
        if blob is not None:
            data, mime = blob
            parts.append({"inline_data": {"mime_type": mime, "data": data}})
        parts.append({"text": prompt})
        client = genai.Client(api_key=key)
        resp = client.models.generate_content(
            model=self.model_id,
            contents=[{"role": "user", "parts": parts}],
            config={"temperature": 0},  # deterministic, per the fairness contract
        )
        return resp.text or ""

# --- general frontier brains (open weights), served via Fireworks -------------------
class _FireworksProvider(_Provider):
    """OpenAI-compatible chat completion through Fireworks (one FIREWORKS_API_KEY, many models).

    Stdlib-only (urllib) so the package stays dependency-light. Sends the fixed text prompt
    (the observation's state_text already fully describes the scene); vision is off by default
    because these chat models are not all multimodal - flip send_image once confirmed per model.
    Reasoning output (<think>.../reasoning_content) is handled by LLMBrain._parse.
    """
    env_key = "FIREWORKS_API_KEY"
    base_url = "https://api.fireworks.ai/inference/v1"
    max_tokens = 1024
    send_image = True                     # multimodal: attach the observation image (OOD lives here)

    def _post(self, key: str, prompt: str, image) -> str:
        import json
        import urllib.error
        import urllib.request
        content: object = prompt
        if image is not None:
            blob = _encode_image(image)
            if blob is not None:
                import base64
                data, mime = blob
                b64 = base64.b64encode(data).decode()
                content = [{"type": "text", "text": prompt},
                           {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}]
        payload = {"model": self.model_id, "temperature": 0, "max_tokens": self.max_tokens,
                   "messages": [{"role": "user", "content": content}]}
        req = urllib.request.Request(
            self.base_url + "/chat/completions", method="POST",
            data=json.dumps(payload).encode(),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                     # Fireworks sits behind Cloudflare, which 403s (code 1010) the default
                     # python-urllib UA; send an explicit one.
                     "User-Agent": "rsbench/0.1 (+https://github.com/robot-survive-bench)"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            out = json.loads(resp.read())
        msg = out["choices"][0]["message"]
        return msg.get("content") or msg.get("reasoning_content") or ""

    def _complete(self, prompt: str, image=None) -> str:
        import urllib.error
        key = os.environ.get(self.env_key)
        if not key:
            raise RuntimeError(f"set {self.env_key} to run {self.name}")
        use_image = image if self.send_image else None
        try:
            return self._post(key, prompt, use_image)
        except urllib.error.HTTPError as exc:
            # a text-only model rejects the image part -> fall back to text so the run continues
            if use_image is not None and exc.code in (400, 415, 422):
                return self._post(key, prompt, None)
            raise RuntimeError(f"{self.name} HTTP {exc.code}: {exc.read()[:200]!r}") from exc


# send_image reflects a probed fact: kimi-k3 / qwen3p8-max read the image (answered a colour test);
# glm-5p2 / deepseek-v4-pro accept the payload but are text-blind here, so we do not send pixels.
class GLM(_FireworksProvider):
    name, model_id, is_open_weight, send_image = "glm", "accounts/fireworks/models/glm-5p2", True, False

class Kimi(_FireworksProvider):
    name, model_id, is_open_weight, send_image = "kimi", "accounts/fireworks/models/kimi-k3", True, True

class Qwen(_FireworksProvider):
    name, model_id, is_open_weight, send_image = "qwen", "accounts/fireworks/models/qwen3p8-max", True, True

class DeepSeek(_FireworksProvider):
    name, model_id, is_open_weight, send_image = "deepseek", "accounts/fireworks/models/deepseek-v4-pro", True, False

class Llama(_Provider):
    # not served on the current Fireworks account; needs a Together/Meta key when available
    name, model_id, env_key, is_open_weight = "llama", "llama-4", "TOGETHER_API_KEY", True

# --- robot-specialized brains (open) ---
class CosmosReason1(_Provider):
    name, model_id, env_key, is_open_weight = "cosmos-reason1", "nvidia/Cosmos-Reason1-7B", "NVIDIA_API_KEY", True

class RoboBrain2(_Provider):
    name, model_id, env_key, is_open_weight = "robobrain2", "BAAI/RoboBrain2.0-7B", "HF_TOKEN", True
