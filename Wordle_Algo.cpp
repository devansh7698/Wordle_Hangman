#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <cmath>
using namespace std;

int vectorToBase3(const vector<int>& vec) {
    int result = 0;
    int base = 1;
    for (int value : vec) {
        result += value * base;
        base *= 3;
    }
    return result;
}

int compareWords(const string& target, const string& guess) {
	vector<int> result(5, 0);
    vector<bool> Matches(5, false);
    for (int i = 0; i < 5; ++i) {
        if (target[i] == guess[i]) {
            result[i] = 2;
            Matches[i] = true;
        }
    }
    for (int i = 0; i < 5; ++i) {
        if (!Matches[i]) {
            for (int j = 0; j < 5; ++j) {
                if (!Matches[j] && target[j] == guess[i]) {
                    result[i] = 1;
                    Matches[j] = true;
                    break;
                }
            }
        }
    }
    return vectorToBase3(result);
}

int t = 0;

void next(vector<int> filter, vector<string> guess_words, vector<vector<int>> comparisonMatrix, string Mystery_Word, int p1) {
    
    if(filter.size() == 1){
        cout << guess_words[filter[0]] << endl;
        t++;
        cout << endl << "Guessed in " << t << " try";
        return;
    }

    int n = guess_words.size();
    string previous_guess = guess_words[p1];
    int result = compareWords(Mystery_Word, previous_guess);

    map<int, double> probability;
    vector<pair<double, string>> entropy;
    for (int i=0; i < guess_words.size(); i++) {
        string guess = guess_words[i];
        for(int j=0; j < filter.size(); j++) {
            int x = filter[j];
            int result = comparisonMatrix[i][x];
            probability[result]++;
        }
        double ent = 0;
        for (const auto& prob : probability) {
            ent = ent - ((prob.second) * log2(prob.second/n) / n);
        }
        entropy.push_back(make_pair(ent, guess));
        probability.clear();
    }
    auto next_it = max_element(entropy.begin(), entropy.end());
    // cout << next_it->first << endl;
    string next_guess = next_it->second;
    int p = next_it - entropy.begin();
    probability.clear();
    entropy.clear();

    result = compareWords(Mystery_Word, next_guess);

    // Next Filter
    vector <int> filter_next;
    for(int i=0; i < filter.size(); i++) {
        int x = filter[i];
        if(comparisonMatrix[x][p] == result){
            filter_next.push_back(x);
        }
    }
    if(filter.size() == filter_next.size()) {
        next_guess = guess_words[filter[0]];
        result = compareWords(Mystery_Word, guess_words[filter[0]]);
        for(int i=0; i < filter.size(); i++) {
            int x = filter[i];
            if(comparisonMatrix[x][p] == result){
                filter_next.push_back(x);
            }
        }
    }

    cout << next_guess << endl;
    t++;

    // Result of Next Guess
    if(result == 242){
        cout << endl << "Guessed in " << t << " try";
        return;
    }

    next(filter_next, guess_words, comparisonMatrix, Mystery_Word, p);
    return;
}

int main() {
    string Dictionary  = "5_Words.txt";
    vector<string> words;
    ifstream inputFile(Dictionary);
    string word;
    while(inputFile >> word) {
    	words.push_back(word);
    }
    vector<string> guess_words = words;
    int n = words.size();
    int m = guess_words.size();


    ifstream binaryFile("data_file.bin", ios::binary);

    binaryFile.read(reinterpret_cast<char*>(&n), sizeof(int));
    binaryFile.read(reinterpret_cast<char*>(&m), sizeof(int));

    vector<std::vector<int>> comparisonMatrix(n, std::vector<int>(m));
    for (int i = 0; i < n; ++i) {
        binaryFile.read(reinterpret_cast<char*>(comparisonMatrix[i].data()), sizeof(int) * m);
    }

    int p1;
    binaryFile.read(reinterpret_cast<char*>(&p1), sizeof(int));

    int first_string_length;
    binaryFile.read(reinterpret_cast<char*>(&first_string_length), sizeof(int));
    string first_string;
    char buffer[256];
    binaryFile.read(buffer, first_string_length);
    first_string.assign(buffer, first_string_length);
    binaryFile.close();

    // Mystery Word Input
    string Mystery_Word;
    cin >> Mystery_Word;

    // First_Guess
    cout << first_string << "(Best Opener)" << endl;
    t++;

    // Result of First_Guess
    int result = compareWords(Mystery_Word, first_string);
    if(result == 242){
        cout << endl << "Guessed in " << t << " try";
        return 0;
    }

    // Filter
    vector <int> filter;
    for(int i=0; i < n; i++) {
        if(comparisonMatrix[i][p1] == result)
            filter.push_back(i);
    }

    next(filter, guess_words, comparisonMatrix, Mystery_Word, p1);

    return 0;
}
