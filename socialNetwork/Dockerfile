# bionic and latest don't work!
FROM yg397/thrift-microservice-deps:xenial


ARG NUM_CPUS=4

COPY ./ /social-network-microservices

# NUM_CPUS is not used in the following 4 commands
RUN cd / && /social-network-microservices/install_clang9toolchain.sh
RUN cd / && /social-network-microservices/build_hiredis.sh
RUN cd / && /social-network-microservices/build_mongoc.sh
RUN cd / && /social-network-microservices/build_redispp.sh

RUN cd /social-network-microservices \
    && rm -rf build 2>/dev/null \
    && mkdir -p build \
    && cd build \
    && cmake -DCMAKE_BUILD_TYPE=Debug .. \
    && make -j${NUM_CPUS} \
    && make install

RUN cd /social-network-microservices/build/src/UniqueIdService \
    && ar x libUniqueIdServiceLLVM.a \
    && llvm-link-9 -o UniqueIdService.bc *.cpp.o

RUN cd /social-network-microservices/build/src/UserService \
    && ar x libUserServiceLLVM.a \
    && llvm-link-9 -o UserService.bc *.cpp.o

RUN cd /social-network-microservices/build/src/SocialGraphService \
    && ar x libSocialGraphServiceLLVM.a \
    && llvm-link-9 -o SocialGraphService.bc *.cpp.o

WORKDIR /social-network-microservices
