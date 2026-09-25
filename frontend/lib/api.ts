export type Movie = {
  movie_id: number;
  title: string;
  genres: string;
  overview: string;
};

export type MovieDetail = Movie & {
  keywords?: string;
  cast?: string;
  director?: string;
};

export type MovieMetadata = {
  movie_id: number;
  poster_url: string | null;
  backdrop_url: string | null;
  release_date: string | null;
  release_year: number | null;
  rating: number | null;
  runtime: number | null;
};

export type MovieWithMetadata = Movie & {
  metadata?: MovieMetadata | null;
};

export type DiscoverMovie = {
  movie_id: number;
  title: string;
  overview: string;
  poster_url: string | null;
  backdrop_url: string | null;
  release_date: string | null;
  release_year: number | null;
  rating: number | null;
  language: string | null;
  genre_ids: number[];
};

export type DiscoverResponse = {
  page: number;
  total_pages: number;
  total_results: number;
  results: DiscoverMovie[];
};

export type TmdbCastMember = {
  name: string;
  character: string;
  profile_path: string | null;
  order: number;
};

export type TmdbCrewMember = {
  name: string;
  job: string;
};

export type TmdbMovieDetail = {
  movie_id: number;
  title: string;
  overview: string;
  poster_url: string | null;
  backdrop_url: string | null;
  release_date: string | null;
  release_year: number | null;
  rating: number | null;
  runtime: number | null;
  genres: string[];
  original_language: string | null;
  production_countries: string[];
  cast: TmdbCastMember[];
  directors: TmdbCrewMember[];
  writers: TmdbCrewMember[];
  key_crew: TmdbCrewMember[];
  similar_movies?: TmdbSimilarMovie[];
};

export type TmdbSimilarMovie = {
  movie_id: number | null;
  title: string;
  overview: string;
  poster_url: string | null;
  backdrop_url: string | null;
  release_date: string | null;
  release_year: number | null;
  rating: number | null;
  runtime: number | null;
  genres: string[];
  original_language: string | null;
  production_countries: string[];
};

export type RecommendationMovie = {
  movie_id: number;
  title: string;
  genres: string;
  overview: string;
  rank?: number;
  similarity?: number;
  match_percentage?: number;
  reasons?: string[];
};

export type RecommendResponse = {
  movie_id: number;
  title: string;
  recommendations: Array<{
    rank: number;
    movie_id: number;
    title: string;
    similarity: number;
    match_percentage?: number;
    reasons?: string[];
  }>;
};

export type MovieListResponse = {
  page: number;
  limit: number;
  total: number;
  total_pages: number;
  results: Movie[];
};

function getApiUrl(): string {
  const url = process.env.NEXT_PUBLIC_API_URL;
  if (!url) {
    throw new Error("NEXT_PUBLIC_API_URL is not set. Check frontend/.env.local");
  }
  return url.replace(/\/$/, "");
}

async function apiGet<T>(path: string, signal?: AbortSignal): Promise<T> {
  const baseUrl = getApiUrl();
  const fullUrl = `${baseUrl}${path}`;

  console.log(`[API] GET ${fullUrl}`);

  try {
    const response = await fetch(fullUrl, {
      cache: "no-store",
      signal,
    });

    console.log(`[API] Response: ${response.status} ${response.statusText} for ${path}`);

    if (!response.ok) {
      let errorBody: string;
      try {
        errorBody = await response.text();
      } catch {
        errorBody = "Could not read error response";
      }
      console.error(`[API] Error response body:`, errorBody);
      throw new Error(`API request failed (${response.status} ${response.statusText}) for ${path}: ${errorBody}`);
    }

    const data = await response.json();
    console.log(`[API] Success:`, path, data);
    return data as T;
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw error;
    }
    if (error instanceof TypeError && error.message.includes("fetch")) {
      console.error(`[API] Network error for ${fullUrl}:`, error);
      throw new Error(`Network error: Unable to connect to ${baseUrl}. Check if backend is running and CORS is configured.`);
    }
    throw error;
  }
}

async function apiPost<T>(path: string, body: any): Promise<T> {
  const baseUrl = getApiUrl();
  const fullUrl = `${baseUrl}${path}`;

  console.log(`[API] POST ${fullUrl}`);

  try {
    const response = await fetch(fullUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      cache: "no-store",
    });

    console.log(`[API] Response: ${response.status} ${response.statusText} for ${path}`);

    if (!response.ok) {
      let errorBody: string;
      try {
        errorBody = await response.text();
      } catch {
        errorBody = "Could not read error response";
      }
      console.error(`[API] Error response body:`, errorBody);
      throw new Error(`API request failed (${response.status} ${response.statusText}) for ${path}: ${errorBody}`);
    }

    const data = await response.json();
    console.log(`[API] Success:`, path, data);
    return data as T;
  } catch (error) {
    if (error instanceof TypeError && error.message.includes("fetch")) {
      console.error(`[API] Network error for ${fullUrl}:`, error);
      throw new Error(`Network error: Unable to connect to ${baseUrl}. Check if backend is running and CORS is configured.`);
    }
    throw error;
  }
}

export function getMovies(page = 1, limit = 20): Promise<MovieListResponse> {
  return apiGet<MovieListResponse>(`/movies?page=${page}&limit=${limit}`);
}

export function getMoviesSearch(query: string, limit = 20): Promise<MovieListResponse> {
  const encodedQuery = encodeURIComponent(query);
  return apiGet<MovieListResponse>(`/movies/search?q=${encodedQuery}&limit=${limit}`);
}

export function getMovie(movie_id: number): Promise<MovieDetail> {
  return apiGet<MovieDetail>(`/movies/${movie_id}`);
}

export function getMovieMetadata(movie_id: number): Promise<MovieMetadata> {
  return apiGet<MovieMetadata>(`/movies/${movie_id}/metadata`);
}

export async function getMovieMetadataBatch(movie_ids: number[]): Promise<Map<number, MovieMetadata | null>> {
  if (movie_ids.length === 0) return new Map();
  
  const results = new Map<number, MovieMetadata | null>();
  try {
    const response = await apiPost<Record<number, MovieMetadata | null>>(
      "/movies/metadata/batch",
      movie_ids
    );
    movie_ids.forEach(id => {
      results.set(id, response[id] ?? null);
    });
  } catch {
    movie_ids.forEach(id => results.set(id, null));
  }
  return results;
}

export function getDiscoverMovies(params: {
  page?: number;
  sort_by?: string;
  year?: number;
  primary_release_year?: number;
  release_date_gte?: string;
  release_date_lte?: string;
  primary_release_date_gte?: string;
  primary_release_date_lte?: string;
  language?: string;
  region?: string;
  with_original_language?: string;
  with_genres?: string;
  vote_average_gte?: number;
  include_adult?: boolean;
  include_video?: boolean;
  with_origin_country?: string;
} = {}, signal?: AbortSignal): Promise<DiscoverResponse> {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      searchParams.set(key, String(value));
    }
  });
  return apiGet<DiscoverResponse>(`/movies/discover?${searchParams.toString()}`, signal);
}

export function getTrendingMovies(time_window: "day" | "week" = "week", language = "en-US", signal?: AbortSignal): Promise<DiscoverResponse> {
  return apiGet<DiscoverResponse>(`/movies/trending?time_window=${time_window}&language=${language}`, signal);
}

export function getPopularMovies(page = 1, params: {
  sort_by?: string;
  year?: number;
  primary_release_year?: number;
  release_date_gte?: string;
  release_date_lte?: string;
  primary_release_date_gte?: string;
  primary_release_date_lte?: string;
  language?: string;
  region?: string;
  with_original_language?: string;
  with_genres?: string;
  vote_average_gte?: number;
  include_adult?: boolean;
  include_video?: boolean;
  with_origin_country?: string;
} = {}, signal?: AbortSignal): Promise<DiscoverResponse> {
  const searchParams = new URLSearchParams({ page: String(page) });
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      searchParams.set(key, String(value));
    }
  });
  return apiGet<DiscoverResponse>(`/movies/popular?${searchParams.toString()}`, signal);
}

export function getUpcomingMovies(page = 1, params: {
  sort_by?: string;
  year?: number;
  primary_release_year?: number;
  release_date_gte?: string;
  release_date_lte?: string;
  primary_release_date_gte?: string;
  primary_release_date_lte?: string;
  language?: string;
  region?: string;
  with_original_language?: string;
  with_genres?: string;
  vote_average_gte?: number;
  include_adult?: boolean;
  include_video?: boolean;
  with_origin_country?: string;
} = {}, signal?: AbortSignal): Promise<DiscoverResponse> {
  const searchParams = new URLSearchParams({ page: String(page) });
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      searchParams.set(key, String(value));
    }
  });
  return apiGet<DiscoverResponse>(`/movies/upcoming?${searchParams.toString()}`, signal);
}

export function getNowPlayingMovies(page = 1, params: {
  sort_by?: string;
  year?: number;
  primary_release_year?: number;
  release_date_gte?: string;
  release_date_lte?: string;
  primary_release_date_gte?: string;
  primary_release_date_lte?: string;
  language?: string;
  region?: string;
  with_original_language?: string;
  with_genres?: string;
  vote_average_gte?: number;
  include_adult?: boolean;
  include_video?: boolean;
  with_origin_country?: string;
} = {}, signal?: AbortSignal): Promise<DiscoverResponse> {
  const searchParams = new URLSearchParams({ page: String(page) });
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      searchParams.set(key, String(value));
    }
  });
  return apiGet<DiscoverResponse>(`/movies/now-playing?${searchParams.toString()}`, signal);
}

export async function getRecommendations(movie_id: number): Promise<RecommendationMovie[]> {
  const response = await apiGet<RecommendResponse>(`/recommend/movie/${movie_id}`);
  return response.recommendations.slice(0, 10).map((rec) => ({
    movie_id: rec.movie_id,
    title: rec.title,
    genres: "",
    overview: "",
    rank: rec.rank,
    similarity: rec.similarity,
    match_percentage: rec.match_percentage,
    reasons: rec.reasons,
  }));
}

export function getTmdbMovie(movie_id: number): Promise<TmdbMovieDetail> {
  return apiGet<TmdbMovieDetail>(`/movies/tmdb/${movie_id}`);
}

// ---------------------------------------------------------------------------
// Find My Movie — POST /recommend/preferences
// ---------------------------------------------------------------------------

export type PreferenceRequest = {
  genres: string[];
  language?: string | null;
  min_rating?: number | null;
  year_from?: number | null;
  year_to?: number | null;
  priority?: string;
  limit?: number;
  exclude_movie_ids?: number[];
};

export type PreferenceRecommendation = {
  movie_id: number;
  title: string;
  match_percentage: number;
  story_similarity: number;
  genre_match: number;
  rating: number | null;
  popularity: number | null;
  release_date: string | null;
  reasons: string[];
};

export type PreferenceResponse = {
  applied_preferences: {
    genres: string[];
    language: string | null;
    min_rating: number | null;
    year_from: number | null;
    year_to: number | null;
    priority: string;
  };
  total: number;
  recommendations: PreferenceRecommendation[];
};

export function getPreferenceRecommendations(
  body: PreferenceRequest
): Promise<PreferenceResponse> {
  return apiPost<PreferenceResponse>("/recommend/preferences", body);
}

// ---------------------------------------------------------------------------
// Mobile catalog — GET /mobiles, /mobiles/search, /mobiles/{phone_id}
// ---------------------------------------------------------------------------
export type Phone = {
  phone_id: number;
  brand: string;
  model: string;
  price_inr: number | null;
  rating: number | null;
  ram_gb: number | null;
  storage_gb: number | null;
  processor_brand: string | null;
  processor_name: string | null;
  core_count: number | null;
  clock_speed_ghz: number | null;
  battery_mah: number | null;
  charging_watt: number | null;
  refresh_rate_hz: number | null;
  rear_camera_mp: number | null;
  front_camera_mp: number | null;
  rear_camera_count: number | null;
  has_5g: boolean;
  has_nfc: boolean;
  os: string | null;
  enrichment?: PhoneEnrichment | null;
};

export type MobileCatalogResponse = {
  page: number;
  limit: number;
  total: number;
  total_pages: number;
  mobiles: Phone[];
};

export type MobileSearchResponse = MobileCatalogResponse;

export function getMobiles(
  page = 1,
  limit = 20,
  signal?: AbortSignal
): Promise<MobileCatalogResponse> {
  const searchParams = new URLSearchParams({ page: String(page), limit: String(limit) });
  return apiGet<MobileCatalogResponse>(`/mobiles?${searchParams.toString()}`, signal);
}

export function searchMobiles(
  params: {
    q?: string | null;
    brand?: string | null;
    min_price?: number | null;
    max_price?: number | null;
    min_ram?: number | null;
    min_storage?: number | null;
    has_5g?: boolean | null;
    page?: number;
    limit?: number;
  } = {},
  signal?: AbortSignal
): Promise<MobileSearchResponse> {
  const searchParams = new URLSearchParams();
  if (params.page) searchParams.set("page", String(params.page));
  if (params.limit) searchParams.set("limit", String(params.limit));
  if (params.q) searchParams.set("q", params.q);
  if (params.brand) searchParams.set("brand", params.brand);
  if (params.min_price !== undefined && params.min_price !== null) searchParams.set("min_price", String(params.min_price));
  if (params.max_price !== undefined && params.max_price !== null) searchParams.set("max_price", String(params.max_price));
  if (params.min_ram !== undefined && params.min_ram !== null) searchParams.set("min_ram", String(params.min_ram));
  if (params.min_storage !== undefined && params.min_storage !== null) searchParams.set("min_storage", String(params.min_storage));
  if (params.has_5g) searchParams.set("has_5g", "true");
  return apiGet<MobileSearchResponse>(`/mobiles/search?${searchParams.toString()}`, signal);
}

export function getMobile(phone_id: number): Promise<Phone> {
  return apiGet<Phone>(`/mobiles/${phone_id}`);
}

// ---------------------------------------------------------------------------
// Find My Phone — POST /recommend/phone/preferences
// ---------------------------------------------------------------------------
export type PhoneRecommendationRequest = {
  budget_max?: number | null;
  budget_min?: number | null;
  brand?: string | null;
  min_ram?: number | null;
  min_storage?: number | null;
  has_5g?: boolean | null;
  refresh_rate_min?: number | null;
  priority?: string;
  limit?: number;
};
export type PhoneEnrichment = {
  canonical_name: string | null;
  model_id: string | null;
  release_date_global: string | null;
  release_date_india: string | null;
  availability_status_india: string | null;
  discontinued_date_india: string | null;

  display_size_inch: number | null;
  display_type: string | null;
  display_resolution: string | null;
  display_refresh_rate_hz: number | string | null;
  display_protection: string | null;
  display_peak_brightness_nits: number | string | null;
  display_hdr_support: string | null;

  rear_camera_count: number | null;
  rear_main_mp: number | null;
  rear_main_aperture: string | null;
  rear_main_sensor: string | null;
  rear_main_ois: string | null;
  rear_ultrawide_mp: number | null;
  rear_ultrawide_aperture: string | null;
  rear_telephoto_mp: number | string | null;
  rear_telephoto_aperture: string | null;
  rear_telephoto_optical_zoom: string | null;
  rear_video_max: string | null;

  front_camera_mp: number | null;
  front_camera_aperture: string | null;
  front_camera_af: string | null;
  front_video_max: string | null;

  battery_type: string | null;
  wired_charging_w: number | string | null;
  wireless_charging_w: number | string | null;
  reverse_wireless_charging_w: number | string | null;
  battery_removable: string | null;

  dimensions_mm: string | null;
  weight_g: number | string | null;
  build_frame: string | null;
  build_back: string | null;
  ip_rating: string | null;
  colors_available: string | null;

  sim_type: string | null;
  five_g_bands: string | null;
  wifi_standard: string | null;
  bluetooth_version: number | string | null;
  usb_version: string | null;
  usb_type: string | null;
  audio_jack: string | null;

  os_launch: string | null;
  os_current: string | null;
  os_update_policy_years: string | null;

  official_product_url: string | null;
  official_image_url: string | null;
  local_image_path: string | null;
  gsmarena_url: string | null;

  launch_price_inr_official: number | null;
  current_min_price_inr: number | null;
  price_updated_at: string | null;
};

export type PhoneRecommendation = Phone & {
  enrichment: PhoneEnrichment | null;
  match_percentage: number;
  gaming_score: number;
  camera_score: number;
  performance_score: number;
  battery_score: number;
  value_score: number;
  student_score: number;
  everyday_score: number;
  reasons: string[];
};

export type PhoneRecommendationResponse = {
  applied_preferences: {
    budget_max?: number | null;
    budget_min?: number | null;
    brand?: string | null;
    min_ram?: number | null;
    min_storage?: number | null;
    has_5g?: boolean | null;
    refresh_rate_min?: number | null;
    priority?: string;
  };
  total: number;
  recommendations: PhoneRecommendation[];
};

export function getPhoneRecommendations(
  body: PhoneRecommendationRequest
): Promise<PhoneRecommendationResponse> {
  return apiPost<PhoneRecommendationResponse>(
    "/recommend/phone/preferences",
    body
  );
}

// ---------------------------------------------------------------------------
// Mobile brands — GET /mobiles/brands
// ---------------------------------------------------------------------------
export type MobileBrandsResponse = {
  brands: string[];
};

export function getMobileBrands(): Promise<MobileBrandsResponse> {
  return apiGet<MobileBrandsResponse>("/mobiles/brands");
}
// ---------------------------------------------------------------------------
// Laptops Module — Types and API Calls
// ---------------------------------------------------------------------------

export type Laptop = {
  laptop_id: number;
  brand: string;
  model: string;
  price_inr: number;
  processor_brand: string;
  processor_model: string;
  cpu_cores: number;
  ram_gb: number;
  ram_type: string;
  storage_gb: number;
  storage_type: string;
  gpu_brand: string;
  gpu_model: string;
  gpu_type: "Integrated" | "Dedicated" | string;
  display_size_inch: number;
  refresh_rate_hz: number;
  resolution: string;
  weight_kg: number;
  battery_whr: number;
  operating_system: string;
  rating: number;
  coding_score?: number;
  gaming_score?: number;
  student_score?: number;
  productivity_score?: number;
  value_score?: number;
  match_percentage?: number;
  reasons?: string[];
};

export type LaptopCatalogResponse = {
  page: number;
  limit: number;
  total: number;
  total_pages: number;
  laptops: Laptop[];
};

export type LaptopRecommendRequest = {
  budget_min?: number | null;
  budget_max?: number | null;
  brand?: string | null;
  min_ram?: number | null;
  gpu_type?: string | null;
  priority?: string;
  limit?: number;
};

export type LaptopRecommendResponse = {
  applied_preferences: {
    budget_min?: number | null;
    budget_max?: number | null;
    brand?: string | null;
    min_ram?: number | null;
    gpu_type?: string | null;
    priority?: string;
  };
  total: number;
  recommendations: Laptop[];
};

export type LaptopBrandsResponse = {
  brands: string[];
};

export function getLaptops(params: {
  page?: number;
  limit?: number;
  brand?: string;
  min_price?: number;
  max_price?: number;
  min_ram?: number;
  gpu_type?: string;
  q?: string;
}): Promise<LaptopCatalogResponse> {
  const q = new URLSearchParams();
  if (params.page) q.set("page", String(params.page));
  if (params.limit) q.set("limit", String(params.limit));
  if (params.brand && params.brand !== "Any Brand") q.set("brand", params.brand);
  if (params.min_price !== undefined) q.set("min_price", String(params.min_price));
  if (params.max_price !== undefined) q.set("max_price", String(params.max_price));
  if (params.min_ram !== undefined) q.set("min_ram", String(params.min_ram));
  if (params.gpu_type && params.gpu_type !== "All") q.set("gpu_type", params.gpu_type);
  if (params.q) q.set("q", params.q);

  const queryStr = q.toString();
  return apiGet<LaptopCatalogResponse>(`/laptops${queryStr ? `?${queryStr}` : ""}`);
}

export function getLaptop(laptopId: number): Promise<Laptop> {
  return apiGet<Laptop>(`/laptops/${laptopId}`);
}

export function getLaptopBrands(): Promise<LaptopBrandsResponse> {
  return apiGet<LaptopBrandsResponse>("/laptops/brands");
}

export function getLaptopRecommendations(
  body: LaptopRecommendRequest
): Promise<LaptopRecommendResponse> {
  return apiPost<LaptopRecommendResponse>("/recommend/laptop/preferences", body);
}