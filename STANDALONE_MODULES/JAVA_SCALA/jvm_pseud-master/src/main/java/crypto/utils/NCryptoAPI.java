package crypto.utils;

//L - library
//K - Key instance
public interface NCryptoAPI<L, K> {
    L getLibraryInstance();

    K getKeyInstance(L libraryInstance);
}
