FROM alpine:3.14

# install sudo as root
RUN apk add --update sudo
RUN sudo apk add bash
ARG USER=floon
ENV HOME /home/$USER
ENV PYTHONUNBUFFERED=1
# add new user
RUN adduser -D $USER \
        && echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER \
        && chmod 0440 /etc/sudoers.d/$USER

USER $USER
WORKDIR $HOME

RUN echo $PATH
ARG DEBIAN_FRONTEND=noninteractive
RUN sudo apk add pulseaudio pulseaudio-alsa
RUN sudo apk add vlc
RUN sudo apk add --update --no-cache python3 && sudo ln -sf python3 /usr/bin/python
ENV PATH="${PATH}:/home/floon/.local/bin"
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .
SHELL ["/bin/bash", "-c", "python3 client.py -s 0.0.0.0"]

