# ****************** TRAINING LOOP - TO DO ON A GPU/TPU ***************************

from transformers import pipeline, TrainingArguments, Trainer
from datasets import load_dataset
from transformers import AutoTokenizer, DataCollatorWithPadding

# Load the summarization pipeline.
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Reports_13F = load_dataset("csv", data_files="output.csv", split="train", column_names=['title', 'body'])
Reports_13F = load_dataset("jkv53/13F_Reports")
checkpoint = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

def tokenize_function(example):
    return tokenizer(example["body"], truncation=True)


tokenized_datasets = Reports_13F.map(tokenize_function, batched=True)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# Create a training arguments object.
training_args = TrainingArguments(
  output_dir="output_dir",
#  num_train_epochs=3,
#  per_device_train_batch_size=16,
  evaluation_strategy="epoch",
  logging_dir="logging_dir",
)

# Create a trainer object.
trainer = Trainer(
  model=summarizer.model,
  args=training_args,
  train_dataset=tokenized_datasets,
  data_collator=data_collator,
  tokenizer=tokenizer,
)

# Fine-tune the model.
trainer.train()

# Evaluate the model.
trainer.evaluate()

# Save the model.
trainer.save_model()
