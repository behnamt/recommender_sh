FROM python:3.6

RUN	pip install -U virtualenv && \
	pip install --upgrade pip

EXPOSE 5055

WORKDIR /usr/src/app

COPY . .

RUN virtualenv venv && \
    /bin/bash -c "source venv/bin/activate" && \
    pip install turicreate && \
    pip install -r requirements.txt

# VOLUME [ "/" ]


# RUN source venv/bin/activate

CMD python api/service.py