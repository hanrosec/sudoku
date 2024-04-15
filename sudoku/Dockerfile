FROM python:latest

COPY . sudoku 
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD [ "flask", "--app", "sudoku", "run", "--host=0.0.0.0" ]