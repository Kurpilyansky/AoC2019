#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <vector>

template<typename T>
std::ostream& operator<<(std::ostream& out, const std::vector<T> &v) {
  out << "[";
  for (const auto & x : v) {
    out << x << " ";
  }
  out << "]";
  return out;
}

void next_phase_fast(std::vector<int32_t> &a) {
  static std::vector<int32_t> pref;
  
  const int32_t n = a.size();
  pref.assign(n + 1, 0);
  for (int32_t i = 0; i < n; ++i) {
    pref[i + 1] = pref[i] + a[i];
  }

  //std::cerr << pref << std::endl;

  for (int32_t i = 0; i < n; ++i) {
    int32_t x = 0;
    int32_t sign = 1;
    int32_t step = 2 * (i + 1);
    for (int32_t j = i; j < n; j += step) {
      int32_t L = j;
      int32_t R = std::min(n, j + i + 1);
      x += sign * (pref[R] - pref[L]);
      sign *= -1;
    }
    a[i] = abs(x) % 10;
  }
  //std::cerr << a << std::endl;
}

std::vector<int32_t> process(const std::vector<int32_t> &a0, const int32_t iters) {
  auto a = a0;
  for (int32_t i = 0; i < iters; ++i) {
    //std::cerr << i << std::endl;
    next_phase_fast(a);
  }
  return a;
}

int main(int argc, char **argv) {
  int32_t TASK = atoi(argv[1]);
  const int32_t iters = atoi(argv[2]);

  static char s[10000];
  assert(scanf("%s", s) == 1);
  int32_t n = strlen(s);
  std::vector<int32_t> a(n);
  for (int32_t i = 0; i < n; ++i) {
    a[i] = s[i] - '0';
  }

  std::cerr << n << " " << a << std::endl;

  if (TASK == 1) {
    auto res = process(a, iters);
    for (int32_t i = 0; i < 8; ++i) {
      std::cout << (int)res[i];
    }
    std::cout << std::endl;
  }

  if (TASK == 2) {
    int32_t message_offset = 0;
    for (int32_t i = 0; i < 7; ++i) {
      message_offset *= 10;
      message_offset += a[i];
    }

    const int32_t TIMES = 10000;
    a.reserve(n * TIMES);
    for (int32_t i = 1; i < TIMES; ++i) {
      a.insert(a.end(), a.begin(), a.begin() + n);
    }
    auto res = process(a, iters);
    for (int32_t i = 0; i < 8; ++i) {
      std::cout << res[i + message_offset];
    }
    std::cout << std::endl;
  }
  return 0;
}
