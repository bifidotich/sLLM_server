import torch
import transformers


def get_model(model_name,
              max_memory_mapping):
    transformers.logging.set_verbosity_error()
    bnb_config = transformers.BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16
    )

    model = transformers.AutoModelForCausalLM.from_pretrained(
        model_name, device_map="auto", max_memory=max_memory_mapping, quantization_config=bnb_config
    )
    tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)

    return model, tokenizer


def generate_response(model,
                      tokenizer,
                      prompt,
                      max_length=1024):
    input_ids = tokenizer(prompt, return_tensors="pt").to(model.device).input_ids
    outputs = model.generate(
        input_ids,
        max_length=max_length,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
        do_sample=True
    )
    response_ids = outputs[0]
    response_text = tokenizer.decode(response_ids, skip_special_tokens=True)
    return response_text
