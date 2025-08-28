FROM quay.io/opendevorg/imagedoesnotexist as first
ARG ZUUL_SIBLINGS=""
RUN echo "Zuul siblings: ${ZUUL_SIBLINGS}"
RUN cp /test-nonce /test-nonce-is-there
COPY . /tmp/src
RUN cp -a /tmp/src/.zuul-siblings/opendev.org/project/fake-sibling/file /target
RUN cp -a /tmp/src/.zuul-siblings/openstack.org/project/fake-sibling/file /target
CMD echo "Zuul container test"; sleep infinity

FROM first as second
RUN echo "This is just to test that loops with siblings work"
