# "Robo Advisor" Project

## Repo Setup

The repository can be accessed at https://github.com/elainezchen/robo-advisor. 

Download or "clone" it onto your computer. Choose a familiar download location like the Desktop. After downloading or cloning the repo, navigate there using the following command line:

```sh
cd ~/Desktop/robo-advisor
```

## Environment Setup

Create and activate new Anaconda virtual environment:

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```
From within the virtual environment, install the required packages specified in the "requirements.txt" file:

```sh
pip install -r requirements.txt
```

To run the Python script from within the virtual environment:
```sh
python app/robo_advisor.py
```

pip install matplotlib

(COPY CREATE ENVIRONMENT FROM CLASS GUIDE)


also instructions on creating environment variable ALPHAVANTAGE_API_KEY

## Usage