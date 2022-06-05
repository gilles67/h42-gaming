FROM ubuntu:22.04 as base

ENV DEBIAN_FRONTEND noninteractive

COPY . /h42gaming

RUN apt-get update -y && apt-get install -y --no-install-recommends make && make -C /h42gaming wheels


FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

COPY . /h42gaming

COPY --from=base /opt/wheels /opt/wheels

RUN apt-get update -y && apt-get install -y --no-install-recommends make && make -C /h42gaming setup

EXPOSE 8000/tcp

WORKDIR /h42gaming

CMD ["/h42gaming/run-console"]