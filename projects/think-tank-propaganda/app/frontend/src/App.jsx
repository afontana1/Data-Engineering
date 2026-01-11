import { useEffect, useMemo, useState } from 'react';
import Highcharts from 'highcharts';
import HighchartsMap from 'highcharts/modules/map';
import HighchartsBoost from 'highcharts/modules/boost';
import HighchartsExporting from 'highcharts/modules/exporting';
import HighchartsExportData from 'highcharts/modules/export-data';
import HighchartsOfflineExporting from 'highcharts/modules/offline-exporting';
import HighchartsReact from 'highcharts-react-official';
import proj4 from 'proj4';
import worldMapRaw from '@highcharts/map-collection/custom/world.geo.json?raw';
import './App.css';

HighchartsMap(Highcharts);
HighchartsBoost(Highcharts);
HighchartsExporting(Highcharts);
HighchartsExportData(Highcharts);
HighchartsOfflineExporting(Highcharts);

const mapData = JSON.parse(worldMapRaw);

const FIELD_ORDER = [
  'institution',
  'org_name',
  'region',
  'location',
  'city',
  'state_province',
  'country',
  'website',
  'sourcewatch_page_url',
];

const FIELD_LABELS = {
  institution: 'Institution',
  org_name: 'Organization',
  region: 'Region',
  location: 'Location',
  city: 'City',
  state_province: 'State/Province',
  country: 'Country',
  website: 'Website',
  sourcewatch_page_url: 'SourceWatch',
};

const WESTERN_EUROPE_COUNTRIES = [
  'united kingdom',
  'ireland',
  'france',
  'germany',
  'netherlands',
  'belgium',
  'luxembourg',
  'switzerland',
  'austria',
  'spain',
  'portugal',
  'italy',
  'denmark',
  'sweden',
  'norway',
  'finland',
  'iceland',
];

const US_STATE_ABBREVS = [
  'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
  'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
  'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
  'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
  'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
  'DC',
];

const CANADA_PROVINCES = [
  'AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE',
  'QC', 'SK', 'YT',
];

const normalizeRegionOnly = (row) => String(row?.region || '').toLowerCase().trim();

const matchesAny = (text, tokens) => tokens.some((token) => text.includes(token));

const normalizeRegionKey = (row) => {
  const region = normalizeRegionOnly(row);
  if (!region) {
    return 'unknown';
  }
  if (region === 'north america') {
    return 'north-america';
  }
  if (region === 'latin america') {
    return 'latin-america';
  }
  if (region === 'europe') {
    return 'europe';
  }
  if (region === 'asia') {
    return 'asia';
  }
  if (region === 'africa') {
    return 'africa';
  }
  if (region === 'middle east') {
    return 'middle-east';
  }
  if (region === 'oceania') {
    return 'oceania';
  }
  if (region === 'apac') {
    return 'asia';
  }
  if (region === 'global') {
    return 'global';
  }
  return 'unknown';
};

const getLocationStateCode = (location) => {
  const match = String(location || '').match(/,\s*([A-Za-z]{2})\b/);
  return match ? match[1].toUpperCase() : '';
};

const isUnitedStates = (row) => {
  const regionKey = normalizeRegionKey(row);
  if (regionKey !== 'north-america' && regionKey !== 'unknown') {
    return false;
  }
  const state = String(row?.state_province || '').trim().toUpperCase();
  if (US_STATE_ABBREVS.includes(state)) {
    return true;
  }
  const locationState = getLocationStateCode(row?.location);
  return US_STATE_ABBREVS.includes(locationState);
};
const isNorthAmerica = (row) => normalizeRegionKey(row) === 'north-america';
const isLatinAmerica = (row) => normalizeRegionKey(row) === 'latin-america';
const isEurope = (row) => normalizeRegionKey(row) === 'europe';
const isAfrica = (row) => normalizeRegionKey(row) === 'africa';
const isMiddleEast = (row) => normalizeRegionKey(row) === 'middle-east';
const isAsia = (row) => normalizeRegionKey(row) === 'asia';
const isOceania = (row) => normalizeRegionKey(row) === 'oceania';
const isGlobal = (row) => normalizeRegionKey(row) === 'global';
const isKnownCategory = (row) => normalizeRegionKey(row) !== 'unknown';

const isWesternEurope = (row) => {
  if (normalizeRegionKey(row) !== 'europe') {
    return false;
  }
  const text = `${row?.location || ''}`.toLowerCase();
  return matchesAny(text, WESTERN_EUROPE_COUNTRIES);
};

const FILTERS = [
  { id: 'all', label: 'All locations', predicate: () => true },
  { id: 'united-states', label: 'United States', predicate: isUnitedStates },
  { id: 'americas', label: 'Americas', predicate: (row) => isNorthAmerica(row) || isLatinAmerica(row) },
  { id: 'north-america', label: 'North America', predicate: isNorthAmerica },
  { id: 'latin-america', label: 'Latin America & Caribbean', predicate: isLatinAmerica },
  { id: 'europe', label: 'Europe & Central Asia', predicate: isEurope },
  { id: 'western-europe', label: 'Western Europe', predicate: isWesternEurope },
  { id: 'africa', label: 'Africa', predicate: isAfrica },
  { id: 'middle-east', label: 'Middle East & North Africa', predicate: isMiddleEast },
  { id: 'asia', label: 'Asia & Pacific', predicate: isAsia },
  { id: 'oceania', label: 'Australia & New Zealand', predicate: isOceania },
  { id: 'global', label: 'Global', predicate: isGlobal },
  { id: 'unknown', label: 'Unknown/Uncategorized', predicate: (row) => !isKnownCategory(row) },
];

const resolveFilter = (value) => (
  FILTERS.find((item) => item.id === value)
  || FILTERS.find((item) => item.label.toLowerCase() === String(value || '').toLowerCase())
  || FILTERS[0]
);

const buildRowKey = (row) => String(row.__id ?? '');

const escapeHtml = (value) =>
  String(value || '').replace(/[&<>"']/g, (char) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  }[char]));

const formatTooltip = (point) => {
  const row = point.custom || {};
  const title = escapeHtml(row.location || row.org_name || point.name || 'Location');
  const rows = FIELD_ORDER.map((field) => {
    const value = row[field];
    if (!value) {
      return '';
    }

    const label = FIELD_LABELS[field] || field;
    if (field === 'website' || field.endsWith('_url')) {
      const safeValue = escapeHtml(value);
      return `<div class="tooltip-row"><span>${label}</span><a href="${safeValue}" target="_blank" rel="noreferrer">${safeValue}</a></div>`;
    }

    return `<div class="tooltip-row"><span>${label}</span><span>${escapeHtml(value)}</span></div>`;
  })
    .filter(Boolean)
    .join('');

  return `<div class="tooltip-card"><div class="tooltip-title">${title}</div>${rows}</div>`;
};

export default function App() {
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
  const [rowsWithCoords, setRowsWithCoords] = useState([]);
  const [missingCoords, setMissingCoords] = useState(0);
  const [activeFilter, setActiveFilter] = useState('united-states');
  const [selectedRowKey, setSelectedRowKey] = useState(null);
  const [locationQuery, setLocationQuery] = useState('');
  const [stateQuery, setStateQuery] = useState('');

  useEffect(() => {
    let cancelled = false;
    const controller = new AbortController();
    setLoading(true);
    setErrorMessage('');

    const baseUrl = new URL(import.meta.env.BASE_URL || '/', window.location.href);
    const jsonUrl = new URL('final.json', baseUrl).toString();

    fetch(jsonUrl, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Failed to load data: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        if (cancelled) {
          return;
        }

        if (!Array.isArray(data)) {
          setRowsWithCoords([]);
          setMissingCoords(0);
          setErrorMessage('Failed to parse data.');
          setLoading(false);
          return;
        }

        const rows = data;
        const normalizeField = (value) => String(value || '').replace(/^\ufeff/, '').trim().toLowerCase();
        const sampleRow = rows.find((row) => row && typeof row === 'object');
        const sampleKeys = sampleRow ? Object.keys(sampleRow) : [];
        const sampleFieldMap = new Map(sampleKeys.map((field) => [normalizeField(field), field]));
        const latField = sampleFieldMap.get('lat');
        const lonField = sampleFieldMap.get('lon');

        if (!latField || !lonField) {
          setRowsWithCoords([]);
          setMissingCoords(0);
          setErrorMessage('Missing lat/lon fields.');
          setLoading(false);
          return;
        }

        const nextRowsWithCoords = [];
        let nextMissingCoords = 0;
        let rowId = 0;

        rows.forEach((row) => {
          if (!row || typeof row !== 'object') {
            nextMissingCoords += 1;
            return;
          }

          const rawLat = row[latField];
          const rawLon = row[lonField];
          if (rawLat === '' || rawLat == null || rawLon === '' || rawLon == null) {
            nextMissingCoords += 1;
            return;
          }

          const lat = Number(rawLat);
          const lon = Number(rawLon);
          if (!Number.isFinite(lat) || !Number.isFinite(lon)) {
            nextMissingCoords += 1;
            return;
          }

          rowId += 1;
          nextRowsWithCoords.push({ row: { ...row, __id: rowId }, lat, lon });
        });

        setRowsWithCoords(nextRowsWithCoords);
        setMissingCoords(nextMissingCoords);
      })
      .catch((error) => {
        if (cancelled || error.name === 'AbortError') {
          return;
        }
        console.error('Failed to load JSON', error);
        setRowsWithCoords([]);
        setMissingCoords(0);
        setErrorMessage('Failed to load data.');
        setLoading(false);
      });

    return () => {
      cancelled = true;
      controller.abort();
    };
  }, []);

  const activeFilterDef = resolveFilter(activeFilter);

  const filteredRowsWithCoords = rowsWithCoords.filter(({ row }) => activeFilterDef.predicate(row));

  const tableFilteredRows = filteredRowsWithCoords.filter(({ row }) => {
    const locationValue = String(row.location || row.city || '').toLowerCase();
    const stateValue = String(row.state_province || '').toLowerCase();
    const locationMatch = !locationQuery.trim()
      || locationValue.includes(locationQuery.trim().toLowerCase());
    const stateMatch = !stateQuery.trim()
      || stateValue.includes(stateQuery.trim().toLowerCase());
    return locationMatch && stateMatch;
  });

  const points = tableFilteredRows.map(({ row, lat, lon }) => {
    const rowKey = buildRowKey(row);
    return {
      name: row.location || row.org_name || 'Location',
      custom: row,
      lat,
      lon,
      rowKey,
      marker: selectedRowKey === rowKey
      ? { radius: 7, lineColor: '#f97316', lineWidth: 2, fillColor: '#fbbf24' }
      : undefined,
    };
  });

  const unmapped = missingCoords;

  useEffect(() => {
    setSelectedRowKey(null);
  }, [activeFilter, locationQuery, stateQuery]);

  useEffect(() => {
    if (!selectedRowKey) {
      return;
    }
    const stillVisible = points.some((point) => point.rowKey === selectedRowKey);
    if (!stillVisible) {
      setSelectedRowKey(null);
    }
  }, [points, selectedRowKey]);

  const options = useMemo(() => ({
    chart: {
      map: mapData,
      backgroundColor: 'transparent',
      spacing: [20, 20, 20, 20],
      animation: false,
      proj4,
    },
    title: {
      text: 'Global Reach of Atlas and SPN',
      style: { color: '#f8fafc', fontSize: '20px', letterSpacing: '0.04em' },
    },
    mapNavigation: {
      enabled: true,
      buttonOptions: {
        theme: {
          fill: '#111827',
          stroke: '#1f2937',
          style: { color: '#e2e8f0' },
        },
      },
    },
    legend: {
      enabled: false,
    },
    boost: {
      enabled: false,
    },
    plotOptions: {
      series: {
        animation: false,
        turboThreshold: 0,
      },
      mappoint: {
        turboThreshold: 0,
      },
    },
    tooltip: {
      useHTML: true,
      backgroundColor: '#0b1020',
      borderColor: '#1f2937',
      shadow: true,
      style: { color: '#e2e8f0' },
      formatter: function () {
        return formatTooltip(this.point);
      },
    },
    series: [
      {
        name: 'World',
        mapData,
        borderColor: '#1f2937',
        nullColor: '#0f172a',
        showInLegend: false,
        enableMouseTracking: false,
        dataLabels: {
          enabled: false,
        },
      },
      {
        type: 'mappoint',
        name: 'Organizations',
        data: points,
        color: '#22d3ee',
        dataLabels: {
          enabled: false,
        },
        marker: {
          radius: 4,
          lineColor: '#0f766e',
          lineWidth: 1,
          fillColor: '#22d3ee',
        },
      },
    ],
  }), [points]);

  const activeFilterLabel = activeFilterDef.label;

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Atlas SPN Location Explorer</h1>
          <p>Hover a point to see organization details.</p>
        </div>
        <div className="status">
          {loading
            ? 'Loading data...'
            : errorMessage || `${points.length} mapped (${activeFilterLabel}), ${unmapped} without coordinates`}
        </div>
      </header>
      <section className="filters">
        <label className="filter-label" htmlFor="region-filter">Filter view</label>
        <select
          id="region-filter"
          className="filter-select"
          value={activeFilter}
          onChange={(event) => setActiveFilter(event.target.value)}
        >
          {FILTERS.map((filter) => (
            <option key={filter.id} value={filter.id}>{filter.label}</option>
          ))}
        </select>
      </section>
      <section className="map-card">
        <HighchartsReact
          highcharts={Highcharts}
          constructorType="mapChart"
          options={options}
          containerProps={{ style: { height: '70vh', width: '100%' } }}
        />
      </section>
      <section className="table-card">
        <div className="table-header">
          <h2>Plotted Locations</h2>
          <span>{tableFilteredRows.length} locations ({activeFilterLabel})</span>
        </div>
        <div className="table-controls">
          <label className="table-filter-label" htmlFor="location-filter">Location</label>
          <input
            id="location-filter"
            className="table-filter-input"
            type="text"
            placeholder="City or location"
            value={locationQuery}
            onChange={(event) => setLocationQuery(event.target.value)}
          />
          <label className="table-filter-label" htmlFor="state-filter">State/Province</label>
          <input
            id="state-filter"
            className="table-filter-input"
            type="text"
            placeholder="State or province"
            value={stateQuery}
            onChange={(event) => setStateQuery(event.target.value)}
          />
        </div>
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Organization</th>
                <th>Location</th>
                <th>Region</th>
                <th>State/Province</th>
                <th>Website</th>
              </tr>
            </thead>
            <tbody>
              {tableFilteredRows.map(({ row }, index) => {
                const website = row.website || '';
                const rowKey = buildRowKey(row);
                return (
                  <tr
                    key={rowKey}
                    className={selectedRowKey === rowKey ? 'is-selected' : ''}
                    onClick={() => setSelectedRowKey(rowKey)}
                  >
                    <td>{index + 1}</td>
                    <td>{row.org_name || row.institution || 'Unknown'}</td>
                    <td>{row.location || 'Unknown'}</td>
                    <td>{row.region || 'Unknown'}</td>
                    <td>{row.state_province || '—'}</td>
                    <td>
                      {website
                        ? (
                          <a href={website} target="_blank" rel="noreferrer">
                            {website}
                          </a>
                        )
                        : '—'}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
