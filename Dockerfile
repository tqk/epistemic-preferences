
FROM aiplanning/planutils

#maintainer information
LABEL maintainer="Christian Muise (christian.muise@queensu.ca)"

RUN planutils install -f -y rpmep
RUN planutils install -f -y lama

WORKDIR /root/PROJECT

CMD planutils activate
