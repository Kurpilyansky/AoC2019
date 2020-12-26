#include <cassert>
#include <cstdio>
#include <cstring>
#include <vector>
#include <set>
#include <map>

using namespace std;

struct Dist {
  int dist;
  int doors_mask;
};

struct State {
  int keys_mask;
  int pos;

  bool operator < (const State &s) const {
    return std::tie(keys_mask, pos) < std::tie(s.keys_mask, s.pos);
  }
};

int main() {
  static char s[200][200];
  int n{}, m{};
  while (scanf("%s", s[n]) == 1) {
    m = strlen(s[n]);
    n++;
  }
  /*
  printf("%d %d\n", n, m);
  for (int i = 0; i < n; ++i) {
    printf("%s\n", s[i]);
  }
  */

  constexpr int KEYS = 26;
  const int dx[4] = {-1, 1, 0, 0};
  const int dy[4] = {0, 0, -1, 1};

  auto bfs = [&](int x, int y) {
    vector<pair<int, int>> q;
    vector<vector<Dist>> d(n, vector<Dist>(m, {-1, -1}));
    q.push_back({x, y});
    d[x][y] = {0, 0};
    vector<Dist> dist(KEYS, {-1, -1});
    for (int i = 0; i < int(q.size()); ++i) {
      x = q[i].first;
      y = q[i].second;
      if ('a' <= s[x][y] && s[x][y] <= 'z') {
        dist[s[x][y] - 'a'] = d[x][y];
      }
      for (int j = 0; j < 4; ++j) {
        int x1 = x + dx[j];
        int y1 = y + dy[j];
        if (d[x1][y1].dist == -1 && s[x1][y1] != '#') {
          d[x1][y1] = {d[x][y].dist + 1, d[x][y].doors_mask | ('A' <= s[x1][y1] && s[x1][y1] <= 'Z' ? (1 << (s[x1][y1] - 'A')) : 0)};
          q.push_back({x1, y1});
        }
      }
    }
    return dist;
  };

  int all_keys_mask = 0;
  vector<vector<Dist>> dist(KEYS);
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      if ('a' <= s[i][j] && s[i][j] <= 'z') {
        all_keys_mask |= (1 << (s[i][j] - 'a'));
        dist[s[i][j] - 'a'] = bfs(i, j);
      }
    }
  }

  /*
  for (int i = 0; i < KEYS; ++i) {
    if (dist[i].empty()) continue;
    for (int j = 0; j < KEYS; ++j) {
      if (dist[j].empty()) continue;
      printf("(%d %d) ", dist[i][j].dist, dist[i][j].doors_mask);
    }
    printf("\n");
  }
  */

  constexpr int INF = (1 << 28);
  set<pair<int, State>> q;
  map<State, int> d;

  auto relax = [&](const State &state, int newD) {
    auto d_it = d.find(state);
    if (d_it != d.end()) {
      if (d_it->second <= newD) {
        return;
      }
      q.erase({d_it->second, state});
    }
    d[state] = newD;
    q.insert({newD, state});
  };

  {
    int x0, y0;
    for (int i = 0; i < n; ++i) {
      for (int j = 0; j < m; ++j) {
        if (s[i][j] == '@') {
          x0 = i;
          y0 = j;
        }
      }
    }

    auto d = bfs(x0, y0);
    for (int i = 0; i < KEYS; ++i) {
      if (d[i].doors_mask == 0) {
        relax({1 << i, i}, d[i].dist);
      }
    }
  }

  int ans = INF;
  while (true) {
    assert(!q.empty());
    auto it = q.begin();
    auto curD = it->first;
    auto cur_keys_mask = it->second.keys_mask;
    auto cur_pos = it->second.pos;
    q.erase(it);

    if (cur_keys_mask == all_keys_mask) {
      ans = curD;
      break;
    }

    for (int next_pos = 0; next_pos < KEYS; ++next_pos) {
      if (next_pos & (1 << cur_keys_mask)) {
        continue;
      }
      auto delta = dist[cur_pos][next_pos].dist;
      auto need_keys_mask = dist[cur_pos][next_pos].doors_mask;
      if ((need_keys_mask & cur_keys_mask) != need_keys_mask) {
        continue;
      }

      relax({cur_keys_mask | (1 << next_pos), next_pos}, curD + delta);
    }
  }

  printf("%d\n", ans);

  return 0;
}

