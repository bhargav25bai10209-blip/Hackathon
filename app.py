import FieldEntryFlow from "@/components/FieldEntryFlow";
import { listEntries } from "@/lib/repo";
import { computeStats, type EntryStats } from "@/lib/stats";

export const dynamic = "force-dynamic";

const EMPTY_STATS: EntryStats = {
  total: 0,
  agreed: 0,
  agreementRate: 0,
  borderline: 0,
  districts: 0,
  states: 0,
  topBreed: "—",
  distribution: [],
};

export default async function HomePage() {
  let stats = EMPTY_STATS;
  try {
    stats = computeStats(await listEntries(250));
  } catch (error) {
    console.error("Home page stats failed", error);
  }

  const tiles = [
    ["Records in module", String(stats.total)],
    ["AI / enumerator match", `${stats.agreementRate}%`],
    ["Borderline cases", String(stats.borderline)],
    ["Districts covered", String(stats.districts)],
  ];

  return (
    <div className="flex flex-col gap-5">
      <section className="glass animate-rise overflow-hidden p-4 sm:p-5">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-[0.64rem] font-extrabold tracking-[0.16em] text-saffron uppercase">
              AI Field Entry Module
            </p>
            <h2 className="mt-1 text-[1.35rem] leading-tight font-extrabold text-navy sm:text-[1.6rem]">
              Breed identification as a{" "}
              <span className="shimmer-text">second opinion</span>
            </h2>
            <p className="mt-1.5 max-w-xl text-[0.82rem] leading-relaxed font-medium text-muted">
              Capture the animal, let the on-device vision model shortlist three candidate
              breeds, compare against the standard breed plate, then confirm. Every decision
              is stamped with the AI suggestion so misclassification can be audited later.
            </p>
          </div>
          <dl className="grid w-full grid-cols-2 gap-2 sm:w-auto sm:grid-cols-4">
            {tiles.map(([label, value]) => (
              <div
                key={label}
                className="rounded-xl border border-line/80 bg-linear-to-b from-white/90 to-white/60 px-3 py-2.5 text-left"
              >
                <dt className="text-[0.58rem] font-bold tracking-[0.09em] text-muted uppercase">
                  {label}
                </dt>
                <dd className="text-[1.15rem] leading-tight font-extrabold text-forest tabular-nums">
                  {value}
                </dd>
              </div>
            ))}
          </dl>
        </div>
      </section>

      <FieldEntryFlow />
    </div>
  );
}
