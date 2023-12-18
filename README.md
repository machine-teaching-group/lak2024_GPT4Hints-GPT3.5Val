# Automating Human Tutor-Style Programming Feedback: Leveraging GPT-4 Tutor Model for Hint Generation and GPT-3.5 Student Model for Hint Validation

This repository contains the implementation of the algorithm GPT4Hints-GPT3.5Val, introduced in the [LAK 2024](https://www.solaresearch.org/events/lak/lak24/) paper [Automating Human Tutor-Style Programming Feedback: Leveraging GPT-4 Tutor Model for Hint Generation and GPT-3.5 Student Model for Hint Validation](https://arxiv.org/pdf/2310.03780.pdf).

---

### Overview
The repository is structured as follows:
- `src/`: this folder contains the source code of the project.
- `data/`: this folder contains a small sample of the input data used in the project. For each programming task, we provide an obfuscated buggy program and the testsuite used in the experiments.
- `output/`: this folder is a placeholder for the output of the project. Illustrative examples can be found here.


---

### Requirements

The implementation requires Python (version >= 3.9) to run. Essential packages can be installed by running <br /> `pip install -r requirements.txt`.

GPT4Hints-GPT3.5Val requires an OpenAI's API key to query GPT-4 and GPT-3.5. It is assumed this API key is placed in `~/.password.json` in the following format: `{ "openai-api-key": "<Your-API-key>" }`.

The correctness of a generated (repair) program is checked by running the program with a test suite in a Docker sandbox environment. This requires Docker to be installed and Docker images are built. The Docker images can be built with the following commands: <br />`docker build -t basicalgo-docker src/utils/sandbox/docker_BasicAlgo` (for the BasicAlgo dataset), and <br /> `docker build -t datascience-docker src/utils/sandbox/docker_DS/` (for the DataRegex and DataAnalysis datasets).

---

### Applying GPT4Hints-GPT3.5Val on an arbitrary buggy program

The script below exemplifies how to apply GPT4Hints-GPT3.5Val on an arbitrary buggy program for the Palindrome problem in the BasicAlgo dataset.
```
python src/end_to_end/end_to_end.py \
--buggy_program_path data/BasicAlgo_Palindrome/buggy.py \
--dataset BasicAlgo \
--question_id palindrome
```

Similarly, the scripts below exemplify how to apply GPT4Hints-GPT3.5Val for the DataRegex and DataAnalysis datasets, respectively.
```
python src/end_to_end/end_to_end.py \
--buggy_program_path data/DataRegex/buggy.py \
--dataset DataRegex
```

```
python src/end_to_end/end_to_end.py \
--buggy_program_path data/DataAnalysis/buggy.py \
--dataset DataAnalysis
```

---
#### Remarks
In the original paper, we used OpenAI's model IDs `gpt-4-0613` for GPT-4 and `gpt-3.5-turbo-0613` for GPT-3.5. However, taking into account the fact that these model versions may be deprecated in the future, in this public implementation, we set `gpt-4` and `gpt-3.5-turbo` as the default IDs for these models, respectively. These IDs  are expected to always point to the latest stable model versions.