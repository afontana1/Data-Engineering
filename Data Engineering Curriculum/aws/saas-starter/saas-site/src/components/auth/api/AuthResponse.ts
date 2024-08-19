import ApiResponse from "../../util/base_api/ApiResponse";

interface AuthResponse extends ApiResponse {
  token?: string;
}

export default AuthResponse;
