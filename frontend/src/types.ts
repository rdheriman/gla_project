export interface Salle {
  id: number;
  nom: string;
  capacite: number;
  description: string | null;
}

export interface Reservation {
  id: number;
  salle_id: number;
  reservataire: string;
  debut: string;
  fin: string;
  motif: string | null;
}

export interface ReservationCreate {
  salle_id: number;
  reservataire: string;
  debut: string;
  fin: string;
  motif?: string;
}