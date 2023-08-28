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

int main() {
    string Dictionary = "5_Words.txt";
    vector<string> words;
    ifstream inputFile(Dictionary);
    string word;
    while (inputFile >> word) {
        words.push_back(word);
    }

    vector<string> guess_words = words;
    int n = words.size();
    int m = guess_words.size();

    vector<vector<int>> comparisonMatrix(n, vector<int>(m));
    vector<vector<bool>> A(n, vector<bool>(m, false));

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            if (A[i][j])
                continue;
            comparisonMatrix[i][j] = compareWords(words[i], guess_words[j]);
            A[i][j] = true;
        }
    }


    map<int, double> probability;
    vector<pair<double, string>> entropy;
    for (int i=0; i < m; i++) {
        string guess = guess_words[i];
        for(int j=0; j < n; j++) {
            int result = comparisonMatrix[i][j];
            probability[result]++;
        }
        double ent = 0;
        for (const auto& prob : probability) {
            ent = ent - ((prob.second) * log2(prob.second/n) / n);
        }
        entropy.push_back(make_pair(ent, guess));
        probability.clear();
    }
    auto first_guess = max_element(entropy.begin(), entropy.end());
    cout << first_guess->first << endl;
    cout << first_guess->second << endl;
    string first_string = first_guess->second;
    int p1 = first_guess - entropy.begin();
    probability.clear();
    entropy.clear();


    ofstream binaryFile("data_file.bin", ios::binary);

    binaryFile.write(reinterpret_cast<const char*>(&n), sizeof(int));
    binaryFile.write(reinterpret_cast<const char*>(&m), sizeof(int));

    // Save the comparison matrix
    for (const auto& row : comparisonMatrix) {
        binaryFile.write(reinterpret_cast<const char*>(row.data()), sizeof(int) * row.size());
    }

    // Save p1 and first_string
    binaryFile.write(reinterpret_cast<const char*>(&p1), sizeof(int));

    int first_string_length = first_string.size();
    binaryFile.write(reinterpret_cast<const char*>(&first_string_length), sizeof(int));
    binaryFile.write(first_string.c_str(), first_string_length);

    binaryFile.close();

    return 0;
}