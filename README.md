# Wordle_Agent
* Unzip 5_words.txt.zip to get 5_words.txt
* Run Pre_Computation.cpp to get "data_file.bin" . (Will take around 2 min)<br></br>
<b>Wordle_Algo.cpp</b>
* Takes a Mystery_Word from 5_words.txt as input .
* Outputs guess_words until correct guess .<br></br>
<b>test.cpp</b>
* Takes a number as input and then creates a vector of random words from 5_words.txt of that size .
* Outputs the number of tries taken by each test_word , Average Tries Taken by all test_words and Success Rate (Correct Guess within 6 tries ) .
* Takes around 30 min for 500 test_words .