import pandas as pd
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import date
from django.db import transaction
from django.http import JsonResponse
from .models import MMUAssignment, Schedule
from .serializers import MMUAssignmentSerializer, ScheduleSerializer
from rest_framework.pagination import PageNumberPagination

class AssignmentPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200

# ❗ ONLY WORKS IF Schedule MODEL STILL EXISTS
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by('-date')
    serializer_class = ScheduleSerializer
    permission_classes = [AllowAny]

# ---------------- MMU ASSIGNMENT ----------------
class MMUAssignmentViewSet(viewsets.ModelViewSet):
    queryset = MMUAssignment.objects.all()
    serializer_class = MMUAssignmentSerializer 
    # pagination_class = AssignmentPagination

    # def list(self, request, *args, **kwargs):
    #     serializer = MMUAssignmentSerializer(self.get_queryset(), many=True)
    #     return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def upload_mmu_excel(request):
    file = request.FILES.get("file")
    if not file:
        return Response({"detail": "No file uploaded"}, status=400)

    import traceback

    try:
        df = pd.read_excel(file)

        # ---------------- NORMALIZE COLUMN NAMES ----------------
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

        # Flexible column name pick function
        def pick(*names):
            for n in names:
                if n in df.columns:
                    return n
            return None

        district_col   = pick("district_", "district")
        mandal_col     = pick("mandal_name", "mandal")
        mmu_col        = pick("mmu_number", "mmu")
        base_col       = pick("base_location", "base")

        lat1_col       = pick("latitude", "lat")
        long1_col      = pick("longitude", "long")

        phc_col        = pick("phc_name")
        vhc_col        = pick("vhc_name_", "vhc_name")
        vhc_code_col   = pick("vhc_code", "vhc_code_")

        hab_col        = pick("habiatation", "habitation")

        lat2_col       = pick("latitude_2", "latitude2", "latitude")
        long2_col      = pick("longitude_2", "longitude2", "longitude")

        fixed_day_col  = pick("fixed_day")
        week_col       = pick("week")

        # ---------- CLEANER: Remove text and convert to float ----------
        import re
        def clean_coordinate(value):
            try:
                v = str(value).strip()
                v = re.sub(r"[^0-9.\-]", "", v)  # keep only digits, dot, minus
                return float(v) if v else None
            except:
                return None

        # ---------------- SAFE ROW PARSING ----------------
        rows = []
        for _, r in df.iterrows():
            district = str(r.get(district_col, "")).strip()
            mandal = str(r.get(mandal_col, "")).strip()

            # Skip invalid rows
            if not district or not mandal:
                continue

            rows.append({
                "district": district,
                "mandal": mandal,
                "mmu_number": str(r.get(mmu_col, "")).strip(),
                "base_location": str(r.get(base_col, "")).strip(),

                "latitude": clean_coordinate(r.get(lat1_col, "")),
                "longitude": clean_coordinate(r.get(long1_col, "")),

                "phc_name": str(r.get(phc_col, "")).strip(),
                "vhc_name": str(r.get(vhc_col, "")).strip(),
                "vhc_code": str(r.get(vhc_code_col, "")).strip(),
                "habitation": str(r.get(hab_col, "")).strip(),

                "lat2": clean_coordinate(r.get(lat2_col, "")),
                "long2": clean_coordinate(r.get(long2_col, "")),

                "fixed_day": str(r.get(fixed_day_col, "")).strip(),
                "week": str(r.get(week_col, "")).strip(),
            })

        # ---------------- UNIQUE SERVICE NUMBER GENERATION ----------------
        districts = sorted({r["district"] for r in rows})
        district_codes = {
            d: str(i + 1).zfill(2)
            for i, d in enumerate(districts)
        }

        mandal_codes = {}
        for d in districts:
            mandals = sorted({r["mandal"] for r in rows if r["district"] == d})
            mandal_codes[d] = {
                m: str(i + 1).zfill(2)
                for i, m in enumerate(mandals)
            }

        # Sequence counter: (District+Mandal) → count
        seq_counter = {}

        for r in rows:
            d = r["district"]
            m = r["mandal"]

            key = (d, m)
            seq_counter[key] = seq_counter.get(key, 0) + 1

            seq = str(seq_counter[key]).zfill(2)

            dcode = district_codes[d]
            mcode = mandal_codes[d][m]

            # Final unique service_no = DDMMSS (6 digits)
            r["service_no"] = int(dcode + mcode + seq)

        # ---------------- SAVE TO DATABASE ----------------
        with transaction.atomic():
            MMUAssignment.objects.all().delete()
            for r in rows:
                MMUAssignment.objects.create(**r)

        return Response({"detail": "Excel uploaded successfully"}, status=200)

    except Exception as e:
        print("\nUPLOAD ERROR:", e)
        traceback.print_exc()
        return Response({"detail": str(e)}, status=500)

    
@api_view(["PATCH"])
@permission_classes([AllowAny])
def update_mmu(request, pk):
    try:
        assign = MMUAssignment.objects.get(pk=pk)
    except MMUAssignment.DoesNotExist:
        return Response({"detail": "Not found"}, status=404)

    mmu = request.data.get("mmu_number")
    if not mmu:
        return Response({"detail": "MMU number required"}, status=400)

    assign.mmu_number = mmu
    assign.save()
    return Response(MMUAssignmentSerializer(assign).data)

@api_view(["GET"])
@permission_classes([AllowAny])
def service_details(request, service_no):
    obj = get_object_or_404(MMUAssignment, service_no=service_no)
    return Response(MMUAssignmentSerializer(obj).data)

@api_view(["GET"])
@permission_classes([AllowAny])
def mmu_list(request):
    mmus = MMUAssignment.objects.values_list("mmu_number", flat=True).distinct()
    return Response(sorted(list(mmus)))
    
@api_view(["GET"])
@permission_classes([AllowAny])
def mmu_schedules(request, mmu_number):
    try:
        schedules = Schedule.objects.filter(mmu_id=mmu_number)

        data = []
        for s in schedules:
            data.append({
                "id": s.id,
                "date": s.date,
                "village": s.village,
                "route_code": s.route_code,
                "status": s.status,
            })

        return Response(data, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(["GET"])
def camps_by_mmu(request, mmu_number):
    assignments = MMUAssignment.objects.filter(mmu_number=mmu_number)
    return Response(MMUAssignmentSerializer(assignments, many=True).data)

def generate_service_codes(rows):
    # 1. Generate district codes
    districts = sorted({r["district"] for r in rows})
    district_codes = {d: str(i + 1).zfill(2) for i, d in enumerate(districts)}

    # 2. Generate mandal codes per district
    mandal_codes = {}
    for d in districts:
        mandals = sorted({r["mandal"] for r in rows if r["district"] == d})
        mandal_codes[d] = {
            m: str(i + 1).zfill(2)
            for i, m in enumerate(mandals)
        }

    # 3. Assign SAME service_no to every row of the group
    for r in rows:
        d = r["district"]
        m = r["mandal"]

        dcode = district_codes[d]
        mcode = mandal_codes[d][m]

        # FINAL SERVICE CODE = DDMM
        r["service_no"] = int(dcode + mcode)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_all_assignments(request):
    MMUAssignment.objects.all().delete()
    return Response({"detail": "All assignments deleted successfully"})

@api_view(["GET"])
@permission_classes([AllowAny])
def all_assignments(request):
    data = MMUAssignment.objects.all().order_by("service_no")
    serializer = MMUAssignmentSerializer(data, many=True)
    return Response(serializer.data)
