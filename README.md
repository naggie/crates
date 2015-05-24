Crates is a database for your media allowing F2F sharing.

Logical Modules
1. **CAS**: Content addressable store for immutable data (MP3 files etc).
2. **index**: Database of file metadata
3. **Mutators**: Systems which query the database and create new files with better
   metadata.
4. **Crawlers**: Systems that programatically add files (soundcloud, filesystem,
   another crates server)
5. **Mapper**: Part of (1) and (2) which organises files as symlinks on the
   filesystem. Other apps can then use the database.
6. **API**: Remote queries to support authenticated peers. Files can be shared
   between peers. Thanks to immutability, peers are verified backups.



Sets of files can be created to make playlists known as "Crates".

Mutators can add BPM, key and chromaprints for example.
