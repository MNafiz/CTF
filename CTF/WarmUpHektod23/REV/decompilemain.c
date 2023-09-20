int __fastcall main(int argc, const char **argv, const char **envp)
{
  char *v3; // rdx
  FILE *stream; // [rsp+18h] [rbp-218h]
  FILE *streama; // [rsp+18h] [rbp-218h]
  __int64 ptr[66]; // [rsp+20h] [rbp-210h] BYREF

  ptr[65] = __readfsqword(0x28u);
  memset(ptr, 0, 512);
  stream = fopen(argv[1], "r");
  fread(ptr, 0x200uLL, 1uLL, stream);
  fclose(stream);
  remove(argv[1]);
  v3 = (char *)argv[1];
  strcat(v3, ".hack");
  streama = fopen(v3, "w");
  encrypt(ptr, 13LL);
  fprintf(streama, (const char *)ptr);
  fclose(streama);
  return 0;
}