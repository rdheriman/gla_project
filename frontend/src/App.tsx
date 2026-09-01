import {
  type FormEvent,
  useEffect,
  useState,
} from "react";

import {
  createReservation,
  getReservations,
  getSalles,
} from "./api";

import type {
  Reservation,
  Salle,
} from "./types";

import "./App.css";


async function fetchData(): Promise<
  [Salle[], Reservation[]]
> {
  return Promise.all([
    getSalles(),
    getReservations(),
  ]);
}


function App() {
  const [salles, setSalles] = useState<Salle[]>([]);
  const [reservations, setReservations] =
    useState<Reservation[]>([]);

  const [salleId, setSalleId] = useState("");
  const [reservataire, setReservataire] =
    useState("");

  const [debut, setDebut] = useState("");
  const [fin, setFin] = useState("");
  const [motif, setMotif] = useState("");

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);


  async function refreshData() {
    const [
      sallesData,
      reservationsData,
    ] = await fetchData();

    setSalles(sallesData);
    setReservations(reservationsData);
  }


  useEffect(() => {
    let cancelled = false;

    fetchData()
      .then(([
        sallesData,
        reservationsData,
      ]) => {
        if (cancelled) {
          return;
        }

        setSalles(sallesData);
        setReservations(reservationsData);
      })
      .catch((error: unknown) => {
        if (
          !cancelled &&
          error instanceof Error
        ) {
          setMessage(error.message);
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);


  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setMessage("");

    try {
      await createReservation({
        salle_id: Number(salleId),
        reservataire,
        debut: new Date(debut).toISOString(),
        fin: new Date(fin).toISOString(),
        motif: motif || undefined,
      });

      await refreshData();

      setMessage(
        "Réservation créée avec succès.",
      );

      setReservataire("");
      setDebut("");
      setFin("");
      setMotif("");
    } catch (error) {
      if (error instanceof Error) {
        setMessage(error.message);
      } else {
        setMessage(
          "Impossible de créer la réservation.",
        );
      }
    }
  }


  if (loading) {
    return <p>Chargement...</p>;
  }


  return (
    <main className="container">
      <header>
        <h1>Application de réservation de salles</h1>

        <p>
          Gestion des salles et des réservations
        </p>
      </header>

      {message && (
        <div className="message">
          {message}
        </div>
      )}

      <section>
        <h2>Salles disponibles</h2>

        <div className="grid">
          {salles.map((salle) => (
            <article
              key={salle.id}
              className="card"
            >
              <h3>{salle.nom}</h3>

              <p>
                Capacité : {salle.capacite}
              </p>

              {salle.description && (
                <p>{salle.description}</p>
              )}
            </article>
          ))}
        </div>
      </section>

      <section>
        <h2>Nouvelle réservation</h2>

        <form onSubmit={handleSubmit}>
          <label>
            Salle

            <select
              value={salleId}
              onChange={(event) =>
                setSalleId(event.target.value)
              }
              required
            >
              <option value="">
                Sélectionner une salle
              </option>

              {salles.map((salle) => (
                <option
                  key={salle.id}
                  value={salle.id}
                >
                  {salle.nom}
                </option>
              ))}
            </select>
          </label>

          <label>
            Réservataire

            <input
              type="text"
              value={reservataire}
              onChange={(event) =>
                setReservataire(
                  event.target.value,
                )
              }
              required
            />
          </label>

          <label>
            Début

            <input
              type="datetime-local"
              value={debut}
              onChange={(event) =>
                setDebut(event.target.value)
              }
              required
            />
          </label>

          <label>
            Fin

            <input
              type="datetime-local"
              value={fin}
              onChange={(event) =>
                setFin(event.target.value)
              }
              required
            />
          </label>

          <label>
            Motif

            <textarea
              value={motif}
              onChange={(event) =>
                setMotif(event.target.value)
              }
            />
          </label>

          <button type="submit">
            Réserver
          </button>
        </form>
      </section>

      <section>
        <h2>Réservations</h2>

        {reservations.length === 0 ? (
          <p>Aucune réservation.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Salle</th>
                <th>Réservataire</th>
                <th>Début</th>
                <th>Fin</th>
                <th>Motif</th>
              </tr>
            </thead>

            <tbody>
              {reservations.map(
                (reservation) => {
                  const salle = salles.find(
                    (item) =>
                      item.id ===
                      reservation.salle_id,
                  );

                  return (
                    <tr key={reservation.id}>
                      <td>
                        {salle?.nom ??
                          reservation.salle_id}
                      </td>

                      <td>
                        {reservation.reservataire}
                      </td>

                      <td>
                        {new Date(
                          reservation.debut,
                        ).toLocaleString()}
                      </td>

                      <td>
                        {new Date(
                          reservation.fin,
                        ).toLocaleString()}
                      </td>

                      <td>
                        {reservation.motif ?? "-"}
                      </td>
                    </tr>
                  );
                },
              )}
            </tbody>
          </table>
        )}
      </section>
    </main>
  );
}


export default App;