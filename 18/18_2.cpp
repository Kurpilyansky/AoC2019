#include <cassert>
#include <cstdio>
#include <cstring>
#include <vector>
#include <set>
#include <map>
#include <iostream>

using namespace std;

struct Dist {
  int dist;
  int doors_mask;
};

struct State {
  int keys_mask{};
  array<char, 4> pos{};

  bool operator < (const State &s) const {
    return std::tie(keys_mask, pos) < std::tie(s.keys_mask, s.pos);
  }
};

ostream& operator<<(ostream &out, State x) {
  out << "mask " << x.keys_mask << " pos [";
  for (int i = 0; i < 4; ++i) {
    out << (int)x.pos[i] << " ";
  }
  out << "]";
  return out;
}

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
  constexpr int dx[4] = {-1, 1, 0, 0};
  constexpr int dy[4] = {0, 0, -1, 1};
  constexpr int INF = (1 << 28);

  auto bfs = [&](int x, int y) {
    vector<pair<int, int>> q;
    vector<vector<Dist>> d(n, vector<Dist>(m, {INF, -1}));
    q.push_back({x, y});
    d[x][y] = {0, 0};
    vector<Dist> dist(KEYS, {INF, -1});
    for (int i = 0; i < int(q.size()); ++i) {
      x = q[i].first;
      y = q[i].second;
      if ('a' <= s[x][y] && s[x][y] <= 'z') {
        dist[s[x][y] - 'a'] = d[x][y];
      }
      for (int j = 0; j < 4; ++j) {
        int x1 = x + dx[j];
        int y1 = y + dy[j];
        if (d[x1][y1].dist == INF && s[x1][y1] != '#') {
          d[x1][y1] = {d[x][y].dist + 1, d[x][y].doors_mask | ('A' <= s[x1][y1] && s[x1][y1] <= 'Z' ? (1 << (s[x1][y1] - 'A')) : 0)};
          q.push_back({x1, y1});
        }
      }
    }
    return dist;
  };

  vector<vector<Dist>> dist(KEYS);
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

  vector<int> key_in_corner(KEYS, -1);
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

    for (int i = 0; i < 4; ++i) {
      s[x0 + dx[i]][y0 + dy[i]] = '#';
    }

    constexpr int dx2[4] = {-1, 1, -1, 1};
    constexpr int dy2[4] = {-1, -1, 1, 1};
    State st{};
    for (int i = 0; i < 4; ++i) {
      int id = dist.size();
      dist.push_back(bfs(x0 + dx2[i], y0 + dy2[i]));
      st.pos[i] = id;
      for (int j = 0; j < KEYS; ++j) {
        if (dist.back()[j].dist != INF) {
          assert(key_in_corner[j] == -1);
          key_in_corner[j] = i;
        }
      }
    }
    relax(st, 0);
  }
  
  /*
  printf("%d %d\n", n, m);
  for (int i = 0; i < n; ++i) {
    printf("%s\n", s[i]);
  }
  */

  int all_keys_mask = 0;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      if ('a' <= s[i][j] && s[i][j] <= 'z') {
        assert(!(all_keys_mask & (1 << (s[i][j] - 'a'))));
        all_keys_mask |= (1 << (s[i][j] - 'a'));
        dist[s[i][j] - 'a'] = bfs(i, j);
      }
    }
  }

  /*
  for (int i = 0; i < KEYS + 4; ++i) {
    if (dist[i].empty()) continue;
    printf("%d(%c): ", i, i < 26 ? 'a' + i : '0' + i - 26);
    for (int j = 0; j < KEYS; ++j) {
      if (dist[j].empty()) continue;
      if (dist[i][j].dist == INF) { continue; }
      printf("%d(%c) ", j, j < 26 ? 'a' + j : '0' + j - 26);
      printf("(%d %d) ", dist[i][j].dist, dist[i][j].doors_mask);
    }
    printf("\n");
  }
  */


  int ans = INF;
  while (true) {
    assert(!q.empty());
    auto it = q.begin();
    const auto curD = it->first;
    const auto cur = it->second;
    q.erase(it);

    //cout << cur << " " << curD << endl;

    if (cur.keys_mask == all_keys_mask) {
      ans = curD;
      break;
    }

    for (int next_pos = 0; next_pos < KEYS; ++next_pos) {
      if (cur.keys_mask & (1 << next_pos)) {
        continue;
      }
      
      int i = key_in_corner[next_pos];
      if (i == -1) {
        assert((all_keys_mask & (1 << next_pos)) == 0);
        continue;
      }
      //cout << cur << " " << curD << " " << next_pos << endl;

      auto delta = dist[cur.pos[i]][next_pos].dist;
      assert(delta != INF);
      auto need_keys_mask = dist[cur.pos[i]][next_pos].doors_mask;
      if ((need_keys_mask & cur.keys_mask) != need_keys_mask) {
        continue;
      }

      auto next = cur;
      next.keys_mask |= (1 << next_pos);
      next.pos[i] = next_pos;
      relax(next, curD + delta);
    }
  }

  printf("%d\n", ans);

  return 0;
}

