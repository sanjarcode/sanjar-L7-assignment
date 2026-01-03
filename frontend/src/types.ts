export interface Genre {
  id: number;
  name: string;
}

export interface Director {
  id: number;
  name: string;
  movies?: Movie[];
}

export interface Actor {
  id: number;
  name: string;
  movies?: Movie[];
}

export interface Movie {
  id: number;
  title: string;
  release_year: number;
  director?: Director;
  genres: Genre[];
  actors: Actor[];
}
