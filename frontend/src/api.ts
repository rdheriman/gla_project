import type {
  Reservation,
  ReservationCreate,
  Salle,
} from "./types";

const API_URL =
  import.meta.env.VITE_API_URL ??
  "http://localhost:8000";


interface FastAPIValidationError {
  loc?: (string | number)[];
  msg?: string;
  type?: string;
}

interface FastAPIErrorResponse {
  detail?: string | FastAPIValidationError[];
}


async function getErrorMessage(
  response: Response,
): Promise<string> {
  try {
    const data =
      (await response.json()) as FastAPIErrorResponse;

    // Cas :
    // {"detail": "Une réservation existe déjà."}
    if (typeof data.detail === "string") {
      return data.detail;
    }

    // Cas validation FastAPI 422 :
    // {"detail": [{...}, {...}]}
    if (Array.isArray(data.detail)) {
      return data.detail
        .map((error) => {
          const field = error.loc
            ?.filter((item) => item !== "body")
            .join(".");

          if (field && error.msg) {
            return `${field} : ${error.msg}`;
          }

          return (
            error.msg ??
            "Donnée invalide."
          );
        })
        .join("\n");
    }

    return `Erreur HTTP ${response.status}.`;
  } catch {
    return `Erreur HTTP ${response.status}.`;
  }
}


export async function getSalles():
Promise<Salle[]> {
  const response = await fetch(
    `${API_URL}/salles`,
  );

  if (!response.ok) {
    throw new Error(
      await getErrorMessage(response),
    );
  }

  return response.json();
}


export async function getReservations():
Promise<Reservation[]> {
  const response = await fetch(
    `${API_URL}/reservations`,
  );

  if (!response.ok) {
    throw new Error(
      await getErrorMessage(response),
    );
  }

  return response.json();
}


export async function createReservation(
  data: ReservationCreate,
): Promise<Reservation> {
  const response = await fetch(
    `${API_URL}/reservations`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    },
  );

  if (!response.ok) {
    throw new Error(
      await getErrorMessage(response),
    );
  }

  return response.json();
}