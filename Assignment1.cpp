// Q1 - Take 2 integer values in two variables x and y and print their product.
#include<iostream>
using namespace std;
int main(){
    int x=2;
    int y=4;

    int product = x*y;
    cout <<"The Product of " <<x<< " and " <<y<< " is: " <<product<< endl;
    return 0;
}

// Q2 - Print the ASCII value of character ‘U’.
#include<iostream>
using namespace std;
int main(){
    char ch = 'U';
    int asciiValue = static_cast<int>(ch);
    cout << "The ASCII value of character '" << ch << "' is: " << asciiValue << endl;
    return 0;
}

// Q3 - Write a C++ program to take length and breadth of a rectangle and print its area.
#include<iostream>
using namespace std;
int main(){
    int length=7;
    int breadth=4;

    int area= length * breadth;

    cout << "The Area Of the Rectangle is: " << area << endl;
    return 0;
}

// Q4 - Write a C++ program to calculate the cube of a number.
#include<iostream>
using namespace std;
int main(){
    int num=4;
    int cube = num * num * num;

    cout << "The Cube of the number " <<num<< " is: " << cube<<endl;
    return 0; 
}

// Q5 - Write a C++ program to find size of basic data types.
#include<iostream>
using namespace std;
int main(){
    cout<< "Size of fundamental data types :" <<endl;

    cout <<"Size of char: " << sizeof(char) << " bytes " << endl;
    cout <<"Size of short: " << sizeof(short) << " bytes " << endl;
    cout <<"Size of int: " << sizeof(int) << " bytes " << endl;
    cout <<"Size of long: " << sizeof(long) << " bytes " << endl;
    cout <<"Size of long long: " << sizeof(long long) << " bytes " << endl; 
    cout <<"Size of float: " << sizeof(float) << " bytes " << endl;
    cout <<"Size of double: " << sizeof(double) << " bytes " << endl;
    cout <<"Size of long double: " << sizeof(long double) << " bytes " << endl;
    cout <<"Size of bool: " << sizeof(bool) << " bytes " << endl;
    return 0;
   
 }


// Q6 - Write a C++ program to swap two numbers with the help of a third variable.
#include<iostream>
using namespace std;
int main(){
    int a=2;
    int b=3;
    int temp;

    temp =a;

    a = b;;
    b = temp;
    cout << "After Swaping The values are: " << "a = " <<a<< " and b = " <<b << endl;
    return 0;
}