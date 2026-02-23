/* ════════════════════════════════════
   CLINIC FORM — AJAX & UI HELPERS
   File: static/js/clinics/clinic_form.js
════════════════════════════════════ */

(function($) {
    "use strict";

    // ---------- RESET HELPERS ----------
    // Each helper clears the target select and all selects below it in the chain.

    function resetCounty() {
        $('#id_county').empty().append('<option value="">Select County</option>');
        resetSubCounty();
    }

    function resetSubCounty() {
        $('#id_sub_county').empty().append('<option value="">Select Sub-county</option>');
        resetParish();
    }

    function resetParish() {
        $('#id_parish').empty().append('<option value="">Select Parish</option>');
        resetVillage();
    }

    function resetVillage() {
        $('#id_village').empty().append('<option value="">Select Village</option>');
    }

    // ---------- LOGO PREVIEW ----------
    $('#id_logo').on('change', function() {
        var file = this.files[0];
        var $preview = $('#logoPreviewContainer');
        if (file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $preview.html('<img src="' + e.target.result + '" class="img-thumbnail" style="max-height:60px;">');
            };
            reader.readAsDataURL(file);
        } else {
            $preview.html('<i class="fas fa-image fa-2x text-muted"></i>');
        }
    });

    // ---------- LOCATION CASCADE: District → County ----------
    // When district changes, reset everything below it first,
    // then fetch counties for the selected district.
    $('#id_district').on('change', function() {
        var districtId = $(this).val();

        // Always reset all downstream fields immediately
        resetCounty();

        if (!districtId) return;

        $.ajax({
            url: '/clinics/api/counties/?district=' + districtId,
            success: function(data) {
                var $county = $('#id_county');
                $.each(data, function(i, item) {
                    $county.append('<option value="' + item.id + '">' + item.name + '</option>');
                });
            },
            error: function() {
                resetCounty();
            }
        });
    });

    // ---------- LOCATION CASCADE: County → Sub-county ----------
    // When county changes, reset sub-county, parish and village first,
    // then fetch sub-counties for the selected county.
    $('#id_county').on('change', function() {
        var countyId = $(this).val();

        // Always reset all downstream fields immediately
        resetSubCounty();

        if (!countyId) return;

        $.ajax({
            url: '/clinics/api/subcounties/?county=' + countyId,
            success: function(data) {
                var $sub = $('#id_sub_county');
                $.each(data, function(i, item) {
                    $sub.append('<option value="' + item.id + '">' + item.name + '</option>');
                });
            },
            error: function() {
                resetSubCounty();
            }
        });
    });

    // ---------- LOCATION CASCADE: Sub-county → Parish ----------
    // When sub-county changes, reset parish and village first,
    // then fetch parishes for the selected sub-county.
    $('#id_sub_county').on('change', function() {
        var subId = $(this).val();

        // Always reset all downstream fields immediately
        resetParish();

        if (!subId) return;

        $.ajax({
            url: '/clinics/api/parishes/?subcounty=' + subId,
            success: function(data) {
                var $parish = $('#id_parish');
                $.each(data, function(i, item) {
                    $parish.append('<option value="' + item.id + '">' + item.name + '</option>');
                });
            },
            error: function() {
                resetParish();
            }
        });
    });

    // ---------- LOCATION CASCADE: Parish → Village ----------
    // When parish changes, reset village first,
    // then fetch villages for the selected parish.
    $('#id_parish').on('change', function() {
        var parishId = $(this).val();

        // Always reset village immediately
        resetVillage();

        if (!parishId) return;

        $.ajax({
            url: '/clinics/api/villages/?parish=' + parishId,
            success: function(data) {
                var $village = $('#id_village');
                $.each(data, function(i, item) {
                    $village.append('<option value="' + item.id + '">' + item.name + '</option>');
                });
            },
            error: function() {
                resetVillage();
            }
        });
    });

})(jQuery);
