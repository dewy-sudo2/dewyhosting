(function () {
  const WEBHOOK =
    "https://discord.com/api/webhooks/1555990845516415056/jjfgnk_GYcCETOatu4bIkaxSgYOv_paXppbjsUqdu19Zy-sRj4sP-KDNgrpdfy76jzUK";

  const cpuEl = document.getElementById("cpu");
  const ramEl = document.getElementById("ram");
  const diskEl = document.getElementById("disk");
  const modal = document.getElementById("orderModal");
  const form = document.getElementById("orderForm");
  const errEl = document.getElementById("orderErr");
  let kind = "discord";

  function priceOf(cpu, ram, disk) {
    return Math.round(cpu * 40 + ram * 0.6 + disk * 90);
  }

  function specs() {
    if (kind === "discord") return { cpu: 3, ram: 300, disk: 1, label: "Discord csomag" };
    return {
      cpu: Number(cpuEl.value),
      ram: Number(ramEl.value),
      disk: Number(diskEl.value),
      label: "Egyedi csomag",
    };
  }

  function refreshCustom() {
    const cpu = Number(cpuEl.value);
    const ram = Number(ramEl.value);
    const disk = Number(diskEl.value);
    document.getElementById("cpuVal").textContent = cpu + "%";
    document.getElementById("ramVal").textContent = ram + " MB";
    document.getElementById("diskVal").textContent = disk + " GB";
    const base = priceOf(cpu, ram, disk);
    document.getElementById("customPrice").textContent = String(base);
    document.getElementById("helloHint").innerHTML =
      "HELLO20-szal az első rendelés: <strong>" + Math.round(base * 0.8) + " Ft / hó</strong>";
  }

  cpuEl.addEventListener("input", refreshCustom);
  ramEl.addEventListener("input", refreshCustom);
  diskEl.addEventListener("input", refreshCustom);
  refreshCustom();

  function openModal(nextKind) {
    kind = nextKind;
    const s = specs();
    const base = priceOf(s.cpu, s.ram, s.disk);
    document.getElementById("orderTitle").textContent = s.label + " rendelése";
    document.getElementById("orderHint").textContent =
      s.cpu + "% CPU · " + s.ram + " MB RAM · " + s.disk + " GB · 1 Gbps · Frankfurt · listaár " + base + " Ft/hó";
    errEl.textContent = "";
    errEl.classList.remove("okmsg");
    modal.classList.add("open");
    form.serverName.focus();
  }

  document.querySelectorAll("[data-order]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      openModal(btn.getAttribute("data-order"));
    });
  });

  document.getElementById("closeModal").addEventListener("click", function () {
    modal.classList.remove("open");
  });
  modal.addEventListener("click", function (e) {
    if (e.target === modal) modal.classList.remove("open");
  });

  function payloadFromForm() {
    const s = specs();
    return {
      serverName: form.serverName.value.trim(),
      email: form.email.value.trim(),
      coupon: form.coupon.value.trim(),
      acceptedLegal: form.acceptedLegal.checked,
      kind: kind,
      cpu: s.cpu,
      ram: s.ram,
      disk: s.disk,
    };
  }

  async function sendViaApi(data) {
    const res = await fetch("/api/order", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const json = await res.json().catch(function () {
      return {};
    });
    if (!res.ok || !json.ok) {
      throw new Error(json.error || "A rendelés nem ment ki.");
    }
    return json;
  }

  async function sendViaWebhook(data) {
    const s = specs();
    const coupon = data.coupon.toUpperCase();
    const base = priceOf(s.cpu, s.ram, s.disk);
    const discount = coupon === "HELLO20" ? 0.2 : 0;
    const final = Math.round(base * (1 - discount));
    const body = {
      username: "DewyHosting",
      embeds: [
        {
          title: "Új DewyHosting rendelés",
          color: 16744192,
          fields: [
            { name: "Szerver neve", value: data.serverName, inline: true },
            { name: "E-mail", value: data.email, inline: true },
            { name: "Csomag", value: s.label, inline: true },
            { name: "CPU", value: s.cpu + "%", inline: true },
            { name: "RAM", value: s.ram + " MB", inline: true },
            { name: "Tárhely", value: s.disk + " GB", inline: true },
            { name: "Hálózat", value: "1 Gbps", inline: true },
            { name: "Lokáció", value: "Frankfurt, node1", inline: true },
            { name: "Kupon", value: coupon || "—", inline: true },
            { name: "Listaár", value: base + " Ft/hó", inline: true },
            { name: "Fizetendő", value: final + " Ft/hó", inline: true },
          ],
          footer: { text: "DewyHosting · hobbi projekt · Németország, Frankfurt" },
        },
      ],
    };
    const res = await fetch(WEBHOOK, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok && res.type !== "opaque") {
      throw new Error("A Discord értesítés nem ment ki.");
    }
    return { ok: true, price: final, base: base, discount: discount };
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    errEl.classList.remove("okmsg");
    errEl.textContent = "";
    const data = payloadFromForm();
    if (!/^[a-zA-Z0-9][a-zA-Z0-9_-]{1,31}$/.test(data.serverName)) {
      errEl.textContent = "A szerver neve 2–32 karakter: betű, szám, _ vagy -.";
      return;
    }
    if (!data.acceptedLegal) {
      errEl.textContent = "Az adatkezelési tájékoztató elfogadása kötelező.";
      return;
    }
    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    try {
      let result;
      try {
        result = await sendViaApi(data);
      } catch (apiErr) {
        const msg = String(apiErr && apiErr.message ? apiErr.message : "");
        const useWebhook =
          msg === "Failed to fetch" ||
          msg.indexOf("A rendelési csatorna") !== -1 ||
          msg.indexOf("nem ment ki") !== -1;
        if (!useWebhook) throw apiErr;
        result = await sendViaWebhook(data);
      }
      errEl.classList.add("okmsg");
      errEl.textContent =
        "Rendelés elküldve. Tájékoztató ár: " + result.price + " Ft/hó. Discordon jelezzük a folytatást.";
      form.reset();
    } catch (err) {
      errEl.textContent = err.message || "Nem sikerült elküldeni.";
    } finally {
      btn.disabled = false;
    }
  });
})();
