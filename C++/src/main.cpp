#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <list>
#include <queue>
#include <unordered_map>
#include <chrono>
#include <random>



// Declare globals
std::unordered_map<std::string, uint32_t> TITLE_TO_ID;
std::unordered_map<uint32_t, std::string> ID_TO_TITLE;
std::unordered_map<uint32_t, std::list<uint32_t>> GRAPH;

bool SEARCHING;
bool SEARCH_KILLED;


void read_ID_map(std::string path) {
    std::ifstream ID_map_file;
    ID_map_file.open(path);

    std::string line;

    int items_read = 0;

    if (ID_map_file.is_open()) {
        std::cout << "Reading ID map at " << path << " . . ." << std::endl;

        TITLE_TO_ID.clear();
        ID_TO_TITLE.clear();

        while (ID_map_file) {
            std::getline(ID_map_file, line);
            std::istringstream ss(line);

            std::string title;
            uint32_t id;

            ss >> title;
            ss >> id;

            // std::cout << title << std::endl;
            // std::cout << id << std::endl;

            TITLE_TO_ID[title] = id;
            ID_TO_TITLE[id] = title;

            items_read++;

            if (items_read % 1000000 == 0) {
                std::cout << "\titems read: " << items_read << std::endl;
            }
        }
    }

    std::cout << "Successfully read " << TITLE_TO_ID.size() << " items\n\n";
}



void read_link_graph(std::string path) {
    std::ifstream link_graph_file;
    link_graph_file.open(path);

    std::string line;

    int items_read = 0;

    if (link_graph_file.is_open()) {
        std::cout << "Reading Link Graph at " << path << " . . ." << std::endl;

        GRAPH.clear();

        while (link_graph_file) {
            std::getline(link_graph_file, line);
            std::istringstream ss(line);

            uint32_t from;
            std::list<uint32_t> tos;

            std::string temp;
            ss >> temp;

            if (temp.empty()) {     // handle EOF
                continue;
            }

            temp.resize(temp.size() - 1);     // remove trailing ':'
            from = std::stoi(temp);

            uint32_t to;
            while (ss >> to) {
                tos.push_back(to);
            }

            GRAPH[from] = tos;

            // std::cout << from << std::endl;
            // std::cout << tos.size() << std::endl;


            items_read++;

            if (items_read % 1000000 == 0) {
                std::cout << "\titems read: " << items_read << std::endl;
            }
        }
    }

    std::cout << "Successfully read " << GRAPH.size() << " items\n\n";
}



std::optional<std::vector<uint32_t>> shortest_path(uint32_t start, uint32_t goal) {
    std::unordered_map<uint32_t, uint32_t> backlinks;       // keep track of the links we used to reconstruct path

    // BFS from start to goal
    std::queue<uint32_t> queue;
    queue.push(start);

    SEARCHING = true;
    SEARCH_KILLED = false;

    int num_searched = 0;
    bool goal_found = false;
    while (!queue.empty() && !goal_found && !SEARCH_KILLED) {
        uint32_t curr = queue.front();
        queue.pop();

        std::list<uint32_t> links = GRAPH[curr];
        for (uint32_t link : links) {
            // skip link if it has already been visited
            if (backlinks.find(link) != backlinks.end()) { continue; }

            // record the back-link
            backlinks[link] = curr;

            // terminate early if we found the goal
            if (link == goal) {
                goal_found = true;
                break;
            }

            queue.push(link);

            num_searched++;
            if (num_searched % 1000000 == 0) {
                std::cout << "\tpages searched: " << num_searched << std::endl;
            }
        }

    }

    SEARCHING = false;

    if (SEARCH_KILLED) {
        std::cout << "(search killed by user)" << std::endl;
        return std::nullopt;
    }

    if (!goal_found) {
        return std::nullopt;
    }

    // Reconstruct path
    std::list<uint32_t> path;

    uint32_t curr = goal;
    while (curr != start) {
        path.push_front(curr);
        curr = backlinks[curr];
    }
    path.push_front(start);

    return std::vector(path.begin(), path.end());
}

// Iterative Deepening
std::optional<std::vector<uint32_t>> shortest_path_IDS(uint32_t start, uint32_t goal) {
    std::unordered_map<uint32_t, uint32_t> backlinks;       // keep track of the links we used to reconstruct path

    std::stack<std::pair<uint32_t, int>> stack;             // store items as (ID, depth)

    SEARCHING = true;
    SEARCH_KILLED = false;

    bool goal_found = false;
    int depth = 1;
    bool remaining = true;
    while (!goal_found && remaining && !SEARCH_KILLED) {
        // DFS with limited depth
        std::cout << "Searching with depth limit: " << depth << std::endl;

        stack = std::stack<std::pair<uint32_t, int>>();
        backlinks.clear();

        remaining = false;      // track whether we have bottomed out on depth
        int num_searched = 0;
        stack.push(std::pair(start, 0));
        while (!stack.empty() && !goal_found && !SEARCH_KILLED) {
            uint32_t curr = stack.top().first;
            uint32_t curr_depth = stack.top().second;

            // std::cout << curr << std::endl;
            // std::cout << curr_depth << std::endl;

            stack.pop();

            if (curr_depth > depth) {
                remaining = true;
                continue;
            }

            std::list<uint32_t> links = GRAPH[curr];
            for (uint32_t link : links) {
                // skip link if it has already been visited
                if (backlinks.find(link) != backlinks.end()) { continue; }

                // record the back-link
                backlinks[link] = curr;

                // terminate early if we found the goal
                if (link == goal) {
                    goal_found = true;
                    break;
                }

                stack.push(std::pair(link, curr_depth+1));

                num_searched++;
                if (num_searched % 1000000 == 0) {
                    std::cout << "\tpages searched: " << num_searched << std::endl;
                }
            }

        }
        std::cout << "\tpages searched: " << num_searched << std::endl;
        depth++;

        // if the search terminated because we 
        if (stack.empty()) {
            break;
        }
    }

    SEARCHING = false;

    if (SEARCH_KILLED) {
        std::cout << "(search killed by user)" << std::endl;
        return std::nullopt;
    }

    if (!goal_found) {
        return std::nullopt;
    }

    // Reconstruct path
    std::list<uint32_t> path;

    uint32_t curr = goal;
    while (curr != start) {
        path.push_front(curr);
        curr = backlinks[curr];
    }
    path.push_front(start);

    return std::vector(path.begin(), path.end());
}


void play_wiki_game(std::string start_title, std::string goal_title) {
    std::cout << "Finding shortest path from \"" << start_title << "\" to \"" << goal_title << "\" . . ." << std::endl;

    if (TITLE_TO_ID.find(start_title) == TITLE_TO_ID.end()) {
        throw "invalid page title: \"" + start_title + "\"";
    }

    if (TITLE_TO_ID.find(goal_title) == TITLE_TO_ID.end()) {
        throw "invalid page title: \"" + goal_title + "\"";
    }

    uint32_t start = TITLE_TO_ID[start_title];
    uint32_t goal = TITLE_TO_ID[goal_title];

    auto t1 = std::chrono::high_resolution_clock::now();
    auto result = shortest_path(start, goal);
    // auto result = shortest_path_IDS(start, goal);
    auto t2 = std::chrono::high_resolution_clock::now();

    auto elapsed_ms = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1);

    std::cout << std::endl;

    if (!result.has_value()) {
        std::cout << "No path found." << std::endl;
    } else {
        auto path = result.value();

        for (size_t i = 0; i < path.size() - 1; i++) {
            auto id = path[i];
            auto title = ID_TO_TITLE[id];
            std::cout << title << "  ->  ";
        }
        auto title = ID_TO_TITLE[path.back()];
        std::cout << title << std::endl;
    }
    std::cout << "\n(" << elapsed_ms.count() << " ms)" << std::endl;
}


std::random_device rd;      // obtain a random number from hardware
std::mt19937 gen(rd());     // seed the generator

uint32_t random_id() {
    std::uniform_int_distribution<> distr(0, ID_TO_TITLE.size() - 1); // define the range
    return distr(gen);
}


void signal_callback_handler(int signum) {
    if (SEARCHING) {
        SEARCH_KILLED = true;
    } else {
        exit(signum);
    }
}



int main() {
    read_ID_map("../Link-Graph/data/ID_map.txt");
    read_link_graph("../Link-Graph/data/link_graph_IDs.txt");

    // play_wiki_game("Marbles", "Eiffel_Tower");
    // play_wiki_game("Chuck_E._Cheese", "Methamphetamine");
    // play_wiki_game("Carnegie_Mellon_University", "Melon");
    // play_wiki_game("Linear_inequality", "Metrocorp_Bancshares");

    signal(SIGINT, signal_callback_handler);

    std::string start_title;
    std::string goal_title;
    while (true) {
        std::cout << "\n\n\n\n\n\n\n\n\n\n\n\n--- Let's play the Wikipedia Shortest-Path Game! ---\n\n";
        std::cout << "          (leave blank for a random page)\n\n";

        std::cout << "Start page:  ";
        std::getline(std::cin, start_title);

        std::cout << "Goal page:   ";
        std::getline(std::cin, goal_title);
        std::cout << "\n";

        if (start_title.empty()) {
            start_title = ID_TO_TITLE[random_id()];
        }

        if (goal_title.empty()) {
            goal_title = ID_TO_TITLE[random_id()];
        }

        try {
            play_wiki_game(start_title, goal_title);
        } catch (std::string msg) {
            std::cout << "An error occurred: " << msg << std::endl;
        }

        std::cout << "\n(press ENTER to play again)";
        std::string temp;
        std::getline(std::cin, temp);
    }

}
