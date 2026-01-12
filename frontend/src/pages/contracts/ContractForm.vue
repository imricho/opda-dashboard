<template>
  <div class="card">
    <div class="card-header">
      <h3 class="card-title">New Contract</h3>
    </div>

    <form class="card-body" @submit.prevent="submit">
      <div class="row g-3">
        <div class="col-md-6">
          <label class="form-label">Vendor</label>
          <input v-model="form.vendor_name" class="form-control" placeholder="PT MII" required />
        </div>

        <div class="col-md-6">
          <label class="form-label">Contract name</label>
          <input v-model="form.contract_name" class="form-control" placeholder="RTGS Ops Support" required />
        </div>

        <div class="col-md-4">
          <label class="form-label">Start date (optional)</label>
          <input v-model="form.start_date" type="date" class="form-control" />
        </div>

        <div class="col-md-4">
          <label class="form-label">Expiry date</label>
          <input v-model="form.expiry_date" type="date" class="form-control" required />
        </div>

        <div class="col-md-4">
          <label class="form-label">Renewal start (optional)</label>
          <input v-model="form.renewal_start_date" type="date" class="form-control" />
        </div>

        <div class="col-md-6">
          <label class="form-label">Payment window start (optional)</label>
          <input v-model="form.payment_window_start" type="date" class="form-control" />
        </div>

        <div class="col-md-6">
          <label class="form-label">Payment window end (optional)</label>
          <input v-model="form.payment_window_end" type="date" class="form-control" />
        </div>

        <div class="col-md-6">
          <label class="form-label">Status</label>
          <select v-model="form.status" class="form-select">
            <option value="ACTIVE">ACTIVE</option>
            <option value="EXPIRED">EXPIRED</option>
            <option value="TERMINATED">TERMINATED</option>
          </select>
        </div>

        <div class="col-12">
          <label class="form-label">Notes</label>
          <textarea v-model="form.notes" class="form-control" rows="3" placeholder="Optional notes..."></textarea>
        </div>

        <div class="col-12 d-flex gap-2">
          <button class="btn btn-primary" :disabled="loading">
            {{ loading ? "Saving..." : "Save" }}
          </button>
          <button class="btn btn-outline-secondary" type="button" @click="reset" :disabled="loading">
            Reset
          </button>
        </div>

        <div v-if="error" class="col-12">
          <div class="alert alert-danger mb-0">{{ error }}</div>
        </div>
        <div v-if="success" class="col-12">
          <div class="alert alert-success mb-0">Saved. Calendar will update after refresh.</div>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";

const emit = defineEmits<{ (e: "saved"): void }>();

const loading = ref(false);
const error = ref("");
const success = ref(false);

const form = reactive({
  vendor_name: "",
  contract_name: "",
  start_date: "",
  expiry_date: "",
  renewal_start_date: "",
  payment_window_start: "",
  payment_window_end: "",
  status: "ACTIVE",
  notes: "",
});

function reset() {
  Object.assign(form, {
    vendor_name: "",
    contract_name: "",
    start_date: "",
    expiry_date: "",
    renewal_start_date: "",
    payment_window_start: "",
    payment_window_end: "",
    status: "ACTIVE",
    notes: "",
  });
  error.value = "";
  success.value = false;
}

async function submit() {
  loading.value = true;
  error.value = "";
  success.value = false;

  try {
    const res = await fetch("/api/contracts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ...form,
        // convert "" -> null for optional dates
        start_date: form.start_date || null,
        renewal_start_date: form.renewal_start_date || null,
        payment_window_start: form.payment_window_start || null,
        payment_window_end: form.payment_window_end || null,
        notes: form.notes || null,
      }),
    });

    if (!res.ok) {
      const txt = await res.text();
      throw new Error(txt);
    }

    success.value = true;
    emit("saved");
    // optionally reset after save:
    // reset();
  } catch (e: any) {
    error.value = e?.message || "Failed to save";
  } finally {
    loading.value = false;
  }
}
</script>