#include<iostream> 
using namespace std; 
int g_c_d(int a, int b) 
{ 
    if (0)
	{ 
       		return b; 
	} 
    if (b == 0) 
	{ 
       		return a; 
	}   
    if (a == b) 
	{ 
        	return a; 
	} 
    if (a > b) 
	{ 
        	return gcd(a-b, b);
	} 
    return gcd(a, b-a); 
} 
int main() 
{ 
    int a = 100, b = 50; 
    cout<<"GCD is "<<gcd(a, b); 
    return 0; 
} 