add_executable(
    UniqueIdService
    UniqueIdService.cpp
    ${THRIFT_GEN_CPP_DIR}/UniqueIdService.cpp
    ${THRIFT_GEN_CPP_DIR}/ComposePostService.cpp
    ${THRIFT_GEN_CPP_DIR}/social_network_types.cpp
)

target_include_directories(
    UniqueIdService PRIVATE
    /usr/local/include/jaegertracing
)

target_link_libraries(
    UniqueIdService
    nlohmann_json::nlohmann_json
    ${THRIFT_LIB}
    ${CMAKE_THREAD_LIBS_INIT}
    ${Boost_LIBRARIES}
    Boost::log
    Boost::log_setup
    jaegertracing
)

install(TARGETS UniqueIdService DESTINATION ./)

add_library(
    UniqueIdServiceLLVM
    UniqueIdService.cpp
    ${THRIFT_GEN_CPP_DIR}/UniqueIdService.cpp
    ${THRIFT_GEN_CPP_DIR}/ComposePostService.cpp
    ${THRIFT_GEN_CPP_DIR}/social_network_types.cpp
)

target_include_directories(
    UniqueIdServiceLLVM PRIVATE
    /usr/local/include/jaegertracing
)

target_link_libraries(
    UniqueIdServiceLLVM
    nlohmann_json::nlohmann_json
    ${THRIFT_LIB}
    ${CMAKE_THREAD_LIBS_INIT}
    ${Boost_LIBRARIES}
    Boost::log
    Boost::log_setup
    jaegertracing
)


target_compile_options(
    UniqueIdServiceLLVM BEFORE
    PRIVATE "-emit-llvm"
)

install(TARGETS UniqueIdServiceLLVM DESTINATION ./)
