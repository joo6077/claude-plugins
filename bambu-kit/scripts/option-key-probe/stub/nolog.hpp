// 옵션 목록 추출용: 로그 호출을 없앤다. 옵션 등록 결과에는 영향이 없다 (로그는 부작용만 있다)
#pragma once
#include <boost/log/trivial.hpp>
#include <iostream>
#undef BOOST_LOG_TRIVIAL
#define BOOST_LOG_TRIVIAL(lvl) if (true) {} else std::cerr
