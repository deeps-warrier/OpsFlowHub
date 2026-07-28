export default function IPCards({ data }) {
  return (
    <div className="cards ip">
      {Object.entries(data).map(([k,v])=>(
        <div className="card small" key={k}>
          <h4>{k.replace("_"," ")}</h4>
          <p>{v}</p>
        </div>
      ))}
    </div>
  );
}
