# ****************** TRAINING LOOP - TO DO ON A GPU/TPU ***************************

from transformers import pipeline, TrainingArguments, Trainer
from datasets import load_dataset
from transformers import AutoTokenizer, DataCollatorWithPadding

# Load the summarization pipeline.
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Reports_13F = load_dataset("csv", data_files="output_all_with_labels.csv", split="train", column_names=['title', 'body', 'label'])
Reports_13F = load_dataset("jkv53/13F_Reports_with_labels")
Reports_13F = Reports_13F["train"].train_test_split(test_size=0.1)
# print(Reports_13F)

checkpoint = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

def tokenize_function(example):
    return tokenizer(example["body"], example["label"], truncation=True)


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
  train_dataset=tokenized_datasets["train"],
  eval_dataset=tokenized_datasets["test"],
  data_collator=data_collator,
  tokenizer=tokenizer,
)

# Fine-tune the model.
trainer.train()

# Evaluate the model.
trainer.evaluate()

# Save the model.
trainer.save_model()
