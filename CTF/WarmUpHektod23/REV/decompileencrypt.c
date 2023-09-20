__int64 __fastcall encrypt(const char *a1, int a2)
{
  __int64 result; // rax
  unsigned int i; // [rsp+18h] [rbp-8h]
  int v4; // [rsp+1Ch] [rbp-4h]

  v4 = strlen(a1);
  for ( i = 0; ; ++i )
  {
    result = i;
    if ( (int)i >= v4 )
      break;
    if ( a1[i] <= 64 || a1[i] > 90 )
    {
      if ( a1[i] > 96 && a1[i] <= 122 )
        a1[i] = (a1[i] - 97 + a2) % 26 + 97;
    }
    else
    {
      a1[i] = (a1[i] - 65 + a2) % 26 + 65;
    }
  }
  return result;
}