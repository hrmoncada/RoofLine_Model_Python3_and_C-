/* https://www.journaldev.com/39743/getline-in-c-plus-plus
*/

#include <iostream>
#include <string>
#include <vector> //  For std::vector
#include <fstream> // For std::ifstream and std::ofstream
#include <sstream> // Header providing string stream classes:
#include <math.h>

using namespace std;

void print_strings_1D(vector <string> outputs){
    int count = 0;
    cout <<  endl;
    cout << "1D vector length = " <<  outputs.size()<< endl << endl;
//     cout << outputs[outputs.size()-2] << endl;
//     cout << outputs[0] << endl;
// Use a range-based for loop to iterate through the output vector
/*    for (const auto& i : outputs){
//         cout << count <<"). " << i << endl;
        cout << i << " ";
        count++; 
    } */  
    for (int i = 0; i < outputs.size(); i++) { 
        if ( outputs[i].size() != false ){ 
            cout << outputs[i] << " ";
        }
    }  
}
void print_strings_2D(vector< vector <string> > data){
    cout << "2D vector (rows, cols) = " << "("<< data.size()<< ", "<< data[0].size() << ")"<< endl << endl;
// Use a range-based for loop to iterate through the output vector
    for (int i = 0; i < data.size(); i++){
        cout << i <<"). "; 
          for (int j = 0; j < data[0].size(); j++){
              cout << data[i][j] << " "; 
//               cout << data[i][data[0].size() - 2] << " "; 
         }     
         cout << endl;
    }   
}
/*-------------------------------------------------------------------------------
 Split string using a delimiter and return a 1D vector
-------------------------------------------------------------------------------- */ 
vector <string>  split_string_line (string line, char delimiter) {
// Create the file object (input) using the string "line"    
    stringstream input(line);
// Select no empty token      
    string token;
// Store the contents into a vector of strings    
    vector <string>  outputs;
//Type (1) -> "getline()", Extracts characters from file "line" and stores them into the string "token" UNTIL the delimitation character "delim" is found.    
    while (getline(input, token, delimiter)) {//while-loop over the string
//        for (const auto& i : token){ cout << i << " "; } 
// Select no empty token 
         if (token.size() != 0)
// Add to the list of output strings            
            outputs.push_back (token);
    }   
//     print_strings_1D(outputs);
    return outputs;
}
/*---------------------------------------------------------------------------------
Subrotine send a string to be split in words using a delimiter,
 Split string using a delimiter and return a 1D vector
-------------------------------------------------------------------------------- */
vector < vector <string> > split_with_delimiter_and_search_pattern(string path_name, string pattern_name) {

// Create the file object (input)
   ifstream infile(path_name);  
   
// Select no empty line/token   
   string line;  
   
// Store the contents into a 2D vector of strings
   vector< vector <string> > data;
   
// Delimiter    
   char delimiter;

//Type (2) -> "getline()", Extracts characters from the file "infile" and stores them into the string "line" UNTIL default character newline '\n' is found, and until end-of-file (EOF)
   while(getline(infile, line)){ // while-loop over the file
// Store the contents into a 1D vector of strings
       vector <string>  outputs1;
       vector <string>  outputs2;
// "line.find()", find the first occurrence of the sub-string "pattern_name" in the string "line", "string::npos" means until the end of the string "line".  
       if (size_t pos = line.find(pattern_name) != string::npos) {
// Select the appropied delimiter to split the line string           
         if (pattern_name == "invocations") {
// Delimiter
             delimiter = ',';             
// Split string using a delimiter            
             outputs1 = split_string_line (line, delimiter);
// Select no empty token      
             string token;      
// Constructs a stringstream object allowing to read the string as if it were a stream (like cin)             
             stringstream input(outputs1[outputs1.size()-1]);
// Delimiter
             delimiter = ' ';  
             
//Type (1) -> "getline()", Extracts characters from file "line" and stores them into the string "token" UNTIL the delimitation character "delim" is found.            
             while (getline(input, token, delimiter)) {//while-loop over the string
// Select no empty token          
                 if (token.size() != 0)
// Add to the list of output strings            
                    outputs2.push_back (token);
             }
//           print_strings_1D(outputs2);
// Add a 1D vectors strings "output" intto a 2D vector strings "data"            
             data.push_back(outputs2);
        } else { 
// Delimiter
             delimiter = ' ';             
// Split string using a delimiter            
             outputs1 = split_string_line (line, delimiter);
// Select no empty token      
             string token;      
// Constructs a stringstream object allowing to read the string as if it were a stream (like cin)             
             stringstream input(outputs1[outputs1.size()-1]);
// Delimiter
             delimiter = ',';  
             
//Type (1) -> "getline()", Extracts characters from file "line" and stores them into the string "token" UNTIL the delimitation character "delim" is found.            
             while (getline(input, token, delimiter)) {//while-loop over the string
// Select no empty token          
                 if (token.size() != 0)
// Add to the list of output strings            
                    outputs2.push_back (token);
             }
          //print_strings_1D(outputs2);
// Add a 1D vectors strings "output" intto a 2D vector strings "data"            
             data.push_back(outputs2);         
             
       } // end-if-else  
       } // end-if  
    } // end-while 
    
//     cout << endl;
//     print_strings_2D(data);
    
    return data;
}

/*----------------------------------------------------
 Extrac RUN_TIME data from results.stats.csv
----------------------------------------------------*/
vector <double>  extract_runtime(string path_runtime, vector <string> &kernels){
    vector <double > RUN_TIME;
//     printf(" \nkernelname Calls TotalDurationNs  AverageNs\n");

//  data temporaly store pattern's information     
    vector < vector <string> > data;  
    
    for (int i = 0; i < kernels.size(); i++){
// call search_pattern_and_st]ore_in_data subroutine
       data = split_with_delimiter_and_search_pattern(path_runtime, kernels[i]);
//        float(data[i][2]);
//        float(data[i][3]);
// stdo(), Convert string to double
       double RUNS = stod(data[0][2]);

//      cout << " " << kernels[i] << "   " << data[0][1] << "    " << data[0][2] << "     " << data[0][3] << endl;

       RUN_TIME.push_back(RUNS);
    } // end  for i
    
//     printf("\nkernels | TotalDurationNs  \n");
//     for (int i = 0; i < RUN_TIME.size(); i++){
//        cout << kernels[i] << "   " << RUN_TIME[i] << endl;
//     }   

    return RUN_TIME;

}
/*-------------------------------------------------------------------------------------
 Extract FETCH_SIZE_MOVED, WRITE_SIZE_MOVED, BYTES_MOVED data mmoved from metrics.csv
------------------------------------------------------------------------------------*/
vector < vector <double> >  extract_metrics(string path_name, vector <string> patterns){
// Declare 2D vector to store data size    
   vector < vector <double> > metrics;

   double BYTES;
   
//  2D vector data temporaly store pattern's information     
    vector < vector <string> > data; 
    
    for (int i = 0; i < patterns.size(); i++){
// Search filen for expecific pattern and ouput vector array Data 
       data = split_with_delimiter_and_search_pattern(path_name, patterns[i]);

       double FETCH_SIZE = 0.0;
       double WRITE_SIZE = 0.0;
       
       for (int j = 0; j < data.size(); j++){ // stdo(), Convert string to double
          FETCH_SIZE += stod(data[j][data[j].size()-2]); //colm 18,
          WRITE_SIZE += stod(data[j][data[j].size()-1]); //colm 19
       }   // end for j

       BYTES = 1024*(FETCH_SIZE + WRITE_SIZE);
       
//  1D vector output temporaly store pattern's information 
       vector <double> output;
       output.push_back(FETCH_SIZE);
       output.push_back(WRITE_SIZE);
       output.push_back(BYTES);
       metrics.push_back(output);
       output.clear();  // clear the vector
    } // end for i

//     printf("kernel     | FETCH_SIZE    |    WRITE_SIZE   | 1024*(FETCH_SIZE + WRITE_SIZE)\n");
//     for (int i = 0; i < metrics.size(); i++){
//        cout << patterns[i] << "  " ;
//        for (int j = 0; j < metrics[i].size(); j++){
//             printf(" %f   ", metrics[i][j]);
//         }
//         printf("\n");
//     }
    return metrics;
}
/*----------------------------------------------------
 Get the Flops Average
----------------------------------------------------*/
vector <double>  extract_FLOPS_average(vector <string> &paths, vector <string> &kernels, vector <string> &patterns){  
   int num_rows;
   int num_cols; 
// Initialize average array size
   double Average[20][4];
// Declare 1D vector integer to store data size   
   vector <double> NFLOPS;  // Store the average FLOPS
   
// For-Loop over files "paths" : data/exess.w150.****.ncu-dpflops.out  
   for (int i = 0; i < paths.size(); i++) {  
//  data temporaly store pattern's information     
        vector < vector <string> > data;   
// For-Loop over searching "patterns" : (dadd, dfma, dmul)
       for (int j = 0; j < patterns.size(); j++) {    
// Store the contents into a 2D vector of strings
          data = split_with_delimiter_and_search_pattern(paths[i], patterns[j]);
//           cout << endl;
          //print_strings_2D(data);

          if (patterns[j] == "invocations") {
             for (int k = 0; k < data.size(); k++){ // stdo(), Convert string to double
                Average[k][j] = stod(data[k][data[k].size() - 2]);
                //printf("(k, j) = (%d, %d), invocation  = %3.1f\n",k, j, Average[k][j]);
             } //end-for-loop k   
          } else {
                for (int k = 0; k < data.size(); k++){ // stdo(), Convert string to double    
                 Average[k][j] = stod(data[k][data[k].size()-1]);
                 //printf("(k, j) = (%d, %d), average  = %f\n",k, j, Average[k][j]);
             } //end-for-loop k
          }//end-if-else        
       }// End For-loop  j
// Get the number of rows and columns
        num_rows = data.size();
        num_cols = data[0].size();
/*        cout << "(num rows, num cols) = " <<  "(" << num_rows <<", " << num_cols << ")" << endl;
        printf("# [ Invocation |   dadd   |   dfma    |  dmul  ]\n");
        for (int i = 0; i < num_rows; i++){ 
           cout << i << "). ";
           for (int j = 0; j < patterns.size(); j++) {
              cout << Average[i][j] << "    ";
           }
           cout << endl;
        }*/      
       
        double FLOPS = 0.0;
        for (int line = 0; line < num_rows; line++){
           FLOPS += Average[line][0]*(Average[line][1] + 2*Average[line][2] + Average[line][3]);
        }// end-for-loop k 
//         printf("%s - FLOPS = %f\n",kernels[i].c_str(), FLOPS);
        NFLOPS.push_back(FLOPS); 
 
   }// End For-loop  i
   
//Insert FLOPS value for the kernel "1_0_0_0"  at position 1 in vector NFLOPS
        NFLOPS.insert(NFLOPS.begin()+1, 2812154194667); 
    
//Insert kernel label "1_0_0_0" into vector string  "kernel_names"  
       kernels.insert(kernels.begin()+1, "1_0_0_0");  
//        for (int line = 0; line < kernels.size(); line++){
//            printf("%s - FLOPS = %f\n",kernels[line].c_str(), NFLOPS[line]);
//        }    
       return {NFLOPS};
}    

/*---------------------------------------------------------------------------------
Main program
-------------------------------------------------------------------------------- */
int main() {   
/* Paths to the data input files */  
   vector <string> paths = {
                      "rerooineperformancemodelplot/exess.w150.0000.ncu-dpflops.out",
                      "rerooineperformancemodelplot/exess.w150.1100.ncu-dpflops.out",
                      "rerooineperformancemodelplot/exess.w150.1110.ncu-dpflops.out"     
                      };
/* Kernel names */    
   vector <string> kernels = {"0_0_0_0","1_1_0_0","1_1_1_0"};// kernel label "1_0_0_0" will be insert later
   
/* Search patters names*/
   vector <string> patterns = {"invocations","dadd", "dfma", "dmul"};
      
// Store the Average FLOPS
   vector <double> NFLOPS = extract_FLOPS_average(paths, kernels, patterns);
   
   printf("| kernelname | Num of FLOPS |\n");
   for (int i = 0; i < NFLOPS.size(); i++)
       printf("  %s    %10.1f\n", kernels[i].c_str(), NFLOPS[i]);
   cout << endl;
//-------------------------------------------------------------------------  
// Extract the data move from "metrics"

    string path_metric = "rerooineperformancemodelplot/metrics.csv";

    vector < vector <double> > metrics  =  extract_metrics(path_metric, kernels);

    printf("kernels  |  FETCH_SIZE   |   WRITE_SIZE   | 1024*(FETCH_SIZE + WRITE_SIZE)\n");
    for (int i = 0; i < metrics.size(); i++){
       cout << kernels[i] << "  " ;
       for (int j = 0; j < metrics[i].size(); j++){
            printf(" %f   ", metrics[i][j]);
        }
        printf("\n");
    }
    cout << endl;

//-------------------------------------------------------------------------   
// Extract the execution time from "resulta.stat"
    string path_results = "rerooineperformancemodelplot/results.stats.csv";
    
    vector <double>  RUN_TIME = extract_runtime(path_results, kernels);
 
    printf("| kernels | RUN TIME |\n");
    for (int i = 0; i < RUN_TIME.size(); i++){
         cout << " " << kernels[i]<< "  " << RUN_TIME[i] << endl;  
    }
  
/*-------------------------------------------------------------------------
Plotting - The Roofline Model
x-axis - Computational Intensity or Aritmetic_Intensity [FLOP/Bytes]
y-axis - Attainable_Peak_performance [GFLOPS/s] = [FLOPSx10^9/s]
m slope - Bandwidth [GFLOPS/s]/FLOP/Bytes]] = [GBytes/s]
y =  mx + b, where b = 0,
Attainable_Peak_performance =  Bandwidth x Computational Intensity + b
b = 0, Since Attainable Peak Performance is equal zero when Computational Intensity
       is equal to zero
Knee point : Interception betwen the Computational Intensity and Bandwidth
y = mx => x = y/m
Attainable_Peak_performance =  Bandwidth x Computational Intensity
Computational Intensity = Bandwidth / Attainable_Peak_performance
-------------------------------------------------------------------------*/
// Giga FLOP 10^9
  double GIGA =  pow(10,9);

// Tera FLOP 10^12;
  double TERA = pow(10,12);

// Nano seconds 10^-9
  double ns = pow(10, -9);
  cout << endl;
  
// P_max : Peak Performance [TFLOP/s]
  double peak_limited_by_execution = 26.5 * TERA;
  printf("P_peak : Peak Performance = %.2E\n",peak_limited_by_execution);
  cout << endl;
  
// Memory Bandwidth (I.b_s) [TBytes/s]
  double peak_limited_by_data_transfer = 1.6 * TERA;
  printf("Bandwidth = %.2E\n",peak_limited_by_data_transfer);
  cout << endl;
  
// x-axis Aritmetic Intensity [FLOP/Bytes]= [NFLOPS]/[BYTES_MOVED]
  printf("Aritmetic_Intensity = \n");
  double Aritmetic_Intensity[ NFLOPS.size()]; 
  for (int i = 0; i < NFLOPS.size(); i++){
     Aritmetic_Intensity[i] = NFLOPS[i]/metrics[i][2];
     printf ("%f\n",Aritmetic_Intensity[i]);
  }
  cout << endl;
  
//y-axis Attainable Peak Performance [TFLOP/s] = [NFLOPS]/ [RUN_TIME x ns]
  printf("Attainable Peak Performance = \n");
  double Attainable_Peak_Performance[NFLOPS.size()];
  for (int i = 0; i < NFLOPS.size(); i++){
       Attainable_Peak_Performance[i] =  NFLOPS[i]/(RUN_TIME[i] *  ns); 
       printf("%f\n",  Attainable_Peak_Performance[i]);
  }
  cout << endl;
//  Knee point :(x, y) = (x_AI, P_max)
//  Peak_performance =  Bandwidth x Arithmetic Intensity
//  Aritmetic_Intensity = Peak_performance / Bandwidth = [TFLOP/s]/[TBytes/s] = [FLOP/Bytes]
  
  double x_AI = peak_limited_by_execution/peak_limited_by_data_transfer;
  printf("knee point (x_AI, P_peak) = (%5.2f, %.2E)\n",x_AI, peak_limited_by_execution);

// colors = np.array(['red', 'blue', 'green','magenta'])
// markers = np.array(['o', 's', 'd', 'v'])
   return 0;
}
