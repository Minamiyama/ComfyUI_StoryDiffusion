from torch import Tensor, nn
from transformers import CLIPTextModel, CLIPTokenizer, T5EncoderModel, T5Tokenizer


class HFEmbedder(nn.Module):
    def __init__(self, version: str, tokenizer_path,clip_cf,is_clip,quantized_mode, max_length: int, **hf_kwargs):
        super().__init__()
        #self.is_clip = version.startswith("openai")
        self.is_clip=is_clip
        self.quantized_mode=quantized_mode
        self.clip_cf=clip_cf
        self.max_length = max_length
        #self.output_key = "pooler_output" if self.is_clip else "last_hidden_state"
        self.output_key = "pooled_output" if self.is_clip else "cond"

        # if self.is_clip:
        #     self.tokenizer: CLIPTokenizer = CLIPTokenizer.from_pretrained(tokenizer_path, max_length=max_length)
        #     self.hf_module: CLIPTextModel = CLIPTextModel.from_pretrained(version, **hf_kwargs)
        # else:
        #     self.tokenizer: T5Tokenizer = T5Tokenizer.from_pretrained(tokenizer_path, max_length=max_length)
        #     self.hf_module: T5EncoderModel = T5EncoderModel.from_pretrained(version, **hf_kwargs)
        # if self.quantized_mode=="fp8":
        #     from optimum.quanto import freeze, qfloat8, quantize
        #     quantize(self.hf_module, weights=qfloat8)
        #     freeze(self.hf_module)
        #
        # self.hf_module = self.hf_module.eval().requires_grad_(False)

    def forward(self, text: list[str]) -> Tensor:
        # batch_encoding = self.tokenizer(
        #     text,
        #     truncation=True,
        #     max_length=self.max_length,
        #     return_length=False,
        #     return_overflowing_tokens=False,
        #     padding="max_length",
        #     return_tensors="pt",
        # )

        # outputs = self.hf_module(
        #     input_ids=batch_encoding["input_ids"].to(self.hf_module.device),
        #     attention_mask=None,
        #     output_hidden_states=False,
        # )
        tokens = self.clip_cf.tokenize(text)
        outputs = self.clip_cf.encode_from_tokens(tokens, return_pooled=True, return_dict=True)
        # cond = outputs.pop("cond")
        # pooled_output=outputs.pop("pooled_output")
        return outputs.pop(self.output_key)
